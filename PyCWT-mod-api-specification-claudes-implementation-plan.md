# PyCWT-mod REST API Implementation Plan

**Document Version:** 1.0  
**Created:** 3 October 2025  
**Target:** FastAPI-based REST API for hardware-accelerated wavelet analysis  
**Scope:** Complete implementation from specification to production deployment

---

## 🎯 Executive Summary

This implementation plan transforms the PyCWT-mod API specification into a production-ready REST API that exposes hardware-accelerated wavelet coherence analysis (CPU, FPGA, embedded systems) through a RESTful interface. The API will integrate with existing pycwt-mod backends while adding real-time streaming capabilities, performance benchmarking, and comprehensive monitoring.

**Timeline:** 6-8 weeks  
**Complexity:** Medium-High (backend integration, hardware detection, async processing)  
**Risk Level:** Medium (hardware dependencies, performance validation)

---

## 📋 Implementation Phases

### **Phase 1: Core API Infrastructure (Week 1-2)**

#### **1.1 Project Structure Setup**

```
pycwt-mod/
├── server/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app entry point
│   ├── config.py                  # Environment config
│   ├── dependencies.py            # Dependency injection
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── routes/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── backends.py    # Backend management
│   │   │   │   ├── wavelet.py     # Wavelet endpoints
│   │   │   │   ├── jobs.py        # Batch processing
│   │   │   │   ├── hardware.py    # Hardware detection
│   │   │   │   └── benchmark.py   # Performance testing
│   │   │   │
│   │   │   └── models/
│   │   │       ├── __init__.py
│   │   │       ├── requests.py    # Pydantic request models
│   │   │       ├── responses.py   # Pydantic response models
│   │   │       └── schemas.py     # Shared schemas
│   │   │
│   │   └── websockets/
│   │       ├── __init__.py
│   │       └── streaming.py       # Real-time streaming
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── wavelet_service.py     # Wavelet computation logic
│   │   ├── backend_service.py     # Backend management
│   │   ├── job_service.py         # Job queue management
│   │   └── hardware_service.py    # Hardware detection
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py            # Auth (future)
│   │   ├── logging.py             # Structured logging
│   │   └── errors.py              # Error handlers
│   │
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py            # Pytest fixtures
│       ├── test_backends.py
│       ├── test_wavelet.py
│       ├── test_jobs.py
│       └── test_integration.py
│
├── .env.example                   # Example environment config
├── docker-compose.yml             # Docker deployment
├── Dockerfile                     # API container
├── requirements-server.txt        # Server dependencies
└── pyproject.toml                # Updated with server extras
```

#### **1.2 Dependencies Installation**

**Core Dependencies (requirements-server.txt):**
```txt
# FastAPI Framework
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.4.0
pydantic-settings>=2.0.3

# Async Support
aiofiles>=23.2.1
python-multipart>=0.0.6

# Job Queue
celery>=5.3.4
redis>=5.0.0

# Monitoring
prometheus-client>=0.18.0
python-json-logger>=2.0.7

# CORS
python-cors>=1.0.0

# PyCWT-mod integration
pycwt-mod>=1.0.0
numpy>=1.24.0
scipy>=1.11.0

# Hardware backends
pyserial>=3.5
joblib>=1.3.0
```

#### **1.3 FastAPI Application Scaffold**

**server/main.py:**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager
import logging

from server.config import settings
from server.api.v1.routes import backends, wavelet, jobs, hardware, benchmark
from server.api.websockets import streaming
from server.core.logging import setup_logging
from server.core.errors import add_exception_handlers

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown lifecycle."""
    logger.info("Starting PyCWT-mod API server...")
    
    # Initialize backends on startup
    from server.services.backend_service import BackendService
    backend_service = BackendService()
    await backend_service.initialize()
    
    yield
    
    # Cleanup on shutdown
    logger.info("Shutting down PyCWT-mod API server...")
    await backend_service.cleanup()


# Create FastAPI app
app = FastAPI(
    title="PyCWT-mod REST API",
    description="Hardware-accelerated wavelet analysis API",
    version="0.1.0-alpha",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gzip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Exception handlers
add_exception_handlers(app)

# Root endpoint
@app.get("/")
async def root():
    return {
        "name": "PyCWT-mod REST API",
        "version": "0.1.0-alpha",
        "docs": "/docs",
        "health": "/health"
    }

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "api_version": "0.1.0-alpha"
    }

# Include routers
app.include_router(backends.router, prefix="/api/v1", tags=["backends"])
app.include_router(wavelet.router, prefix="/api/v1", tags=["wavelet"])
app.include_router(jobs.router, prefix="/api/v1", tags=["jobs"])
app.include_router(hardware.router, prefix="/api/v1", tags=["hardware"])
app.include_router(benchmark.router, prefix="/api/v1", tags=["benchmark"])

# WebSocket endpoint
app.include_router(streaming.router, prefix="/ws", tags=["streaming"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "server.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
```

#### **1.4 Configuration Management**

**server/config.py:**
```python
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """Application settings."""
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    # Backends
    DEFAULT_BACKEND: str = "sequential"
    AVAILABLE_BACKENDS: str = "sequential,joblib,elm11"
    
    # Job Management
    MAX_CONCURRENT_JOBS: int = 10
    JOB_TIMEOUT_SECONDS: int = 3600
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Hardware Detection
    HARDWARE_DETECTION_TIMEOUT: int = 5
    ENABLE_FPGA: bool = True
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
```

---

### **Phase 2: Backend Management Endpoints (Week 2)**

#### **2.1 Backend Service**

**server/services/backend_service.py:**
```python
from typing import Dict, List, Optional
import logging
from pycwt_mod.backends import list_backends, get_backend

logger = logging.getLogger(__name__)


class BackendService:
    """Service for managing computation backends."""
    
    def __init__(self):
        self._backends_cache = {}
        self._initialized = False
    
    async def initialize(self):
        """Initialize and cache backend information."""
        logger.info("Initializing backends...")
        
        backend_names = list_backends()
        for name in backend_names:
            try:
                backend = get_backend(name)
                self._backends_cache[name] = {
                    "name": name,
                    "available": backend.is_available(),
                    "description": backend.__doc__ or "No description",
                    "type": backend.__class__.__name__
                }
                logger.info(f"Backend '{name}': available={backend.is_available()}")
            except Exception as e:
                logger.warning(f"Failed to initialize backend '{name}': {e}")
                self._backends_cache[name] = {
                    "name": name,
                    "available": False,
                    "description": "Failed to load",
                    "type": "Unknown",
                    "error": str(e)
                }
        
        self._initialized = True
    
    async def list_all_backends(self) -> List[Dict]:
        """List all registered backends."""
        if not self._initialized:
            await self.initialize()
        
        return list(self._backends_cache.values())
    
    async def get_backend_info(self, name: str) -> Optional[Dict]:
        """Get information about a specific backend."""
        if not self._initialized:
            await self.initialize()
        
        return self._backends_cache.get(name)
    
    async def cleanup(self):
        """Cleanup resources."""
        logger.info("Cleaning up backends...")
        self._backends_cache.clear()
```

#### **2.2 Backend Routes**

**server/api/v1/routes/backends.py:**
```python
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from server.api.v1.models.responses import BackendListResponse, BackendInfoResponse
from server.services.backend_service import BackendService

router = APIRouter()


def get_backend_service():
    """Dependency injection for backend service."""
    return BackendService()


@router.get("/backends/", response_model=BackendListResponse)
async def list_backends(
    backend_service: BackendService = Depends(get_backend_service)
):
    """
    List all available computation backends.
    
    Returns information about each registered backend including:
    - Name and type
    - Hardware/software availability
    - Description and capabilities
    """
    backends = await backend_service.list_all_backends()
    return {"backends": backends}


@router.get("/backends/{backend_name}", response_model=BackendInfoResponse)
async def get_backend(
    backend_name: str,
    backend_service: BackendService = Depends(get_backend_service)
):
    """
    Get detailed information about a specific backend.
    
    Parameters:
    - backend_name: Backend identifier (e.g., 'sequential', 'joblib', 'elm11')
    """
    backend_info = await backend_service.get_backend_info(backend_name)
    
    if backend_info is None:
        raise HTTPException(
            status_code=404,
            detail=f"Backend '{backend_name}' not found"
        )
    
    return backend_info
```

#### **2.3 Response Models**

**server/api/v1/models/responses.py:**
```python
from pydantic import BaseModel, Field
from typing import List, Optional


class BackendInfo(BaseModel):
    """Backend information model."""
    name: str = Field(..., description="Backend identifier")
    available: bool = Field(..., description="Hardware/software availability")
    description: str = Field(..., description="Backend description")
    type: str = Field(..., description="Backend class name")
    error: Optional[str] = Field(None, description="Error message if unavailable")


class BackendListResponse(BaseModel):
    """Response model for listing backends."""
    backends: List[BackendInfo] = Field(..., description="List of available backends")


class BackendInfoResponse(BackendInfo):
    """Response model for single backend information."""
    pass
```

---

### **Phase 3: Wavelet Analysis Endpoints (Week 3)**

#### **3.1 Wavelet Service**

**server/services/wavelet_service.py:**
```python
import numpy as np
import time
import logging
from typing import Tuple, Optional
import pycwt_mod as pycwt

logger = logging.getLogger(__name__)


class WaveletService:
    """Service for wavelet transform computations."""
    
    async def compute_cwt(
        self,
        data: np.ndarray,
        dt: float,
        dj: float = 0.25,
        s0: float = -1,
        J: int = -1,
        mother: str = "morlet",
        param: float = -1
    ) -> dict:
        """
        Compute continuous wavelet transform.
        
        Returns:
        - wave: Wavelet transform coefficients
        - scales: Wavelet scales
        - freqs: Corresponding frequencies
        - coi: Cone of influence
        - fft: FFT of input data
        - fftfreqs: FFT frequencies
        """
        logger.info(f"Computing CWT for {len(data)} points")
        
        start_time = time.time()
        
        try:
            wave, scales, freqs, coi, fft, fftfreqs = pycwt.cwt(
                data, dt, dj=dj, s0=s0, J=J, wavelet=mother, param=param
            )
            
            computation_time = time.time() - start_time
            logger.info(f"CWT completed in {computation_time:.3f}s")
            
            return {
                "wave": wave.tolist(),  # Complex values
                "scales": scales.tolist(),
                "freqs": freqs.tolist(),
                "coi": coi.tolist(),
                "fft": fft.tolist(),
                "fftfreqs": fftfreqs.tolist(),
                "computation_time": computation_time
            }
        
        except Exception as e:
            logger.error(f"CWT computation failed: {e}")
            raise
    
    async def compute_wct(
        self,
        signal1: np.ndarray,
        signal2: np.ndarray,
        dt: float,
        dj: float = 0.25,
        s0: float = -1,
        J: int = -1,
        significance_level: float = 0.95,
        mc_count: int = 300,
        backend: str = "sequential"
    ) -> dict:
        """
        Compute wavelet coherence between two signals.
        
        Returns:
        - WCT: Wavelet coherence transform
        - aWCT: Phase angles
        - coi: Cone of influence
        - freqs: Frequencies
        - signif: Significance levels
        - backend_used: Actual backend used
        - computation_time: Time taken
        """
        logger.info(f"Computing WCT with backend='{backend}', mc_count={mc_count}")
        
        start_time = time.time()
        
        try:
            WCT, aWCT, coi, freqs, sig95 = pycwt.wct(
                signal1, signal2,
                dt=dt, dj=dj, s0=s0, J=J,
                sig=True,
                significance_level=significance_level,
                mc_count=mc_count,
                backend=backend
            )
            
            computation_time = time.time() - start_time
            logger.info(f"WCT completed in {computation_time:.3f}s")
            
            return {
                "WCT": WCT.tolist(),
                "aWCT": aWCT.tolist(),
                "coi": coi.tolist(),
                "freqs": freqs.tolist(),
                "signif": sig95.tolist(),
                "backend_used": backend,
                "computation_time": computation_time
            }
        
        except Exception as e:
            logger.error(f"WCT computation failed: {e}")
            raise
    
    async def compute_xwt(
        self,
        signal1: np.ndarray,
        signal2: np.ndarray,
        dt: float,
        dj: float = 0.25,
        s0: float = -1,
        J: int = -1
    ) -> dict:
        """
        Compute cross-wavelet transform.
        
        Returns:
        - xwt: Cross-wavelet transform
        - phase: Phase angles
        - coi: Cone of influence
        - freqs: Frequencies
        """
        logger.info(f"Computing XWT for signals of length {len(signal1)}")
        
        start_time = time.time()
        
        try:
            xwt, phase, coi, freqs = pycwt.xwt(
                signal1, signal2,
                dt=dt, dj=dj, s0=s0, J=J
            )
            
            computation_time = time.time() - start_time
            logger.info(f"XWT completed in {computation_time:.3f}s")
            
            return {
                "xwt": xwt.tolist(),
                "phase": phase.tolist(),
                "coi": coi.tolist(),
                "freqs": freqs.tolist(),
                "computation_time": computation_time
            }
        
        except Exception as e:
            logger.error(f"XWT computation failed: {e}")
            raise
```

#### **3.2 Wavelet Routes**

**server/api/v1/routes/wavelet.py:**
```python
from fastapi import APIRouter, HTTPException, Depends
from server.api.v1.models.requests import CWTRequest, WCTRequest, XWTRequest
from server.api.v1.models.responses import CWTResponse, WCTResponse, XWTResponse
from server.services.wavelet_service import WaveletService
import numpy as np

router = APIRouter()


def get_wavelet_service():
    """Dependency injection for wavelet service."""
    return WaveletService()


@router.post("/wavelet/cwt", response_model=CWTResponse)
async def continuous_wavelet_transform(
    request: CWTRequest,
    wavelet_service: WaveletService = Depends(get_wavelet_service)
):
    """
    Perform continuous wavelet transform on time series data.
    
    Parameters:
    - data: Time series array
    - dt: Time step
    - dj: Scale resolution (default: 0.25)
    - s0: Smallest scale (auto if -1)
    - J: Number of scales (auto if -1)
    - mother: Wavelet type (default: 'morlet')
    - param: Wavelet parameter (default: -1)
    """
    try:
        data = np.array(request.data)
        
        result = await wavelet_service.compute_cwt(
            data=data,
            dt=request.dt,
            dj=request.dj,
            s0=request.s0,
            J=request.J,
            mother=request.mother,
            param=request.param
        )
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/wavelet/wct", response_model=WCTResponse)
async def wavelet_coherence(
    request: WCTRequest,
    wavelet_service: WaveletService = Depends(get_wavelet_service)
):
    """
    Calculate wavelet coherence between two time series.
    
    Parameters:
    - signal1, signal2: Time series arrays
    - dt: Time step
    - dj: Scale resolution (default: 0.25)
    - significance_level: Significance level (default: 0.95)
    - mc_count: Monte Carlo simulations (default: 300)
    - backend: Computation backend (sequential/joblib/elm11)
    """
    try:
        signal1 = np.array(request.signal1)
        signal2 = np.array(request.signal2)
        
        if len(signal1) != len(signal2):
            raise HTTPException(
                status_code=400,
                detail="signal1 and signal2 must have the same length"
            )
        
        result = await wavelet_service.compute_wct(
            signal1=signal1,
            signal2=signal2,
            dt=request.dt,
            dj=request.dj,
            s0=request.s0,
            J=request.J,
            significance_level=request.significance_level,
            mc_count=request.mc_count,
            backend=request.backend
        )
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/wavelet/xwt", response_model=XWTResponse)
async def cross_wavelet_transform(
    request: XWTRequest,
    wavelet_service: WaveletService = Depends(get_wavelet_service)
):
    """
    Calculate cross-wavelet transform between two time series.
    
    Parameters:
    - signal1, signal2: Time series arrays
    - dt: Time step
    - dj: Scale resolution (default: 0.25)
    """
    try:
        signal1 = np.array(request.signal1)
        signal2 = np.array(request.signal2)
        
        if len(signal1) != len(signal2):
            raise HTTPException(
                status_code=400,
                detail="signal1 and signal2 must have the same length"
            )
        
        result = await wavelet_service.compute_xwt(
            signal1=signal1,
            signal2=signal2,
            dt=request.dt,
            dj=request.dj,
            s0=request.s0,
            J=request.J
        )
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

### **Phase 4: Real-Time Streaming (Week 4)**

#### **4.1 WebSocket Streaming Endpoint**

**server/api/websockets/streaming.py:**
```python
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, Optional
import json
import logging
import numpy as np
from server.services.wavelet_service import WaveletService

logger = logging.getLogger(__name__)
router = APIRouter()


class StreamingManager:
    """Manage real-time wavelet analysis streams."""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.wavelet_service = WaveletService()
    
    async def connect(self, stream_id: str, websocket: WebSocket):
        """Accept new streaming connection."""
        await websocket.accept()
        self.active_connections[stream_id] = websocket
        logger.info(f"Stream {stream_id} connected")
    
    def disconnect(self, stream_id: str):
        """Remove streaming connection."""
        if stream_id in self.active_connections:
            del self.active_connections[stream_id]
            logger.info(f"Stream {stream_id} disconnected")
    
    async def process_chunk(
        self,
        websocket: WebSocket,
        signal1_chunk: np.ndarray,
        signal2_chunk: np.ndarray,
        dt: float,
        backend: str = "sequential"
    ):
        """Process signal chunk and send results."""
        try:
            # Compute wavelet coherence for chunk
            result = await self.wavelet_service.compute_wct(
                signal1=signal1_chunk,
                signal2=signal2_chunk,
                dt=dt,
                backend=backend,
                mc_count=50  # Reduced for real-time
            )
            
            # Send result back to client
            await websocket.send_json({
                "type": "result",
                "data": result
            })
        
        except Exception as e:
            logger.error(f"Error processing chunk: {e}")
            await websocket.send_json({
                "type": "error",
                "message": str(e)
            })


# Global streaming manager
streaming_manager = StreamingManager()


@router.websocket("/stream/wct")
async def websocket_wavelet_coherence(websocket: WebSocket):
    """
    Real-time wavelet coherence streaming endpoint.
    
    This WebSocket endpoint enables continuous processing of signal streams
    for applications requiring low-latency analysis (BCI, adaptive stimulation).
    
    Protocol:
    1. Client sends configuration:
       {"type": "config", "dt": 0.001, "backend": "elm11"}
    
    2. Client sends signal chunks:
       {"type": "data", "signal1": [...], "signal2": [...]}
    
    3. Server responds with results:
       {"type": "result", "data": {...}}
    """
    stream_id = f"stream_{id(websocket)}"
    
    await streaming_manager.connect(stream_id, websocket)
    
    config = {"dt": 0.1, "backend": "sequential"}
    
    try:
        while True:
            # Receive message from client
            message = await websocket.receive_json()
            
            if message["type"] == "config":
                # Update configuration
                config.update(message)
                await websocket.send_json({
                    "type": "ack",
                    "message": "Configuration updated"
                })
            
            elif message["type"] == "data":
                # Process signal chunk
                signal1 = np.array(message["signal1"])
                signal2 = np.array(message["signal2"])
                
                await streaming_manager.process_chunk(
                    websocket=websocket,
                    signal1_chunk=signal1,
                    signal2_chunk=signal2,
                    dt=config["dt"],
                    backend=config.get("backend", "sequential")
                )
            
            elif message["type"] == "ping":
                # Keepalive
                await websocket.send_json({"type": "pong"})
    
    except WebSocketDisconnect:
        streaming_manager.disconnect(stream_id)
    
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        streaming_manager.disconnect(stream_id)
```

---

### **Phase 5: Hardware Detection & Benchmarking (Week 5)**

#### **5.1 Hardware Detection Service**

**server/services/hardware_service.py:**
```python
import logging
import subprocess
from typing import Dict, List
from server.config import settings

logger = logging.getLogger(__name__)


class HardwareService:
    """Service for detecting and managing hardware accelerators."""
    
    async def detect_all_hardware(self) -> Dict:
        """
        Detect all available hardware accelerators.
        
        Returns information about:
        - FPGA devices (Tang Nano 9K)
        - Embedded systems (ELM11)
        - GPU availability
        - CPU capabilities
        """
        logger.info("Running hardware detection...")
        
        results = {
            "fpga": await self._detect_fpga(),
            "embedded": await self._detect_embedded(),
            "gpu": await self._detect_gpu(),
            "cpu": await self._detect_cpu()
        }
        
        return results
    
    async def _detect_fpga(self) -> Dict:
        """Detect FPGA devices (Tang Nano 9K)."""
        try:
            from pycwt_mod.backends import get_backend
            backend = get_backend("elm11")
            
            if backend.is_available():
                return {
                    "available": True,
                    "device": "Tang Nano 9K",
                    "interface": "Serial/USB",
                    "status": "Connected"
                }
            else:
                return {
                    "available": False,
                    "device": "Tang Nano 9K",
                    "status": "Not detected"
                }
        
        except Exception as e:
            logger.warning(f"FPGA detection failed: {e}")
            return {
                "available": False,
                "error": str(e)
            }
    
    async def _detect_embedded(self) -> Dict:
        """Detect embedded systems (ELM11)."""
        try:
            import serial.tools.list_ports
            
            # Look for ELM11-compatible devices
            ports = serial.tools.list_ports.comports()
            embedded_devices = []
            
            for port in ports:
                if "USB" in port.description or "Serial" in port.description:
                    embedded_devices.append({
                        "port": port.device,
                        "description": port.description
                    })
            
            return {
                "available": len(embedded_devices) > 0,
                "devices": embedded_devices
            }
        
        except Exception as e:
            logger.warning(f"Embedded detection failed: {e}")
            return {"available": False, "error": str(e)}
    
    async def _detect_gpu(self) -> Dict:
        """Detect GPU availability."""
        try:
            # Check for CUDA
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                gpu_info = result.stdout.strip().split('\n')
                return {
                    "available": True,
                    "devices": [line.split(',') for line in gpu_info],
                    "type": "NVIDIA CUDA"
                }
        
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        
        return {"available": False, "type": "None"}
    
    async def _detect_cpu(self) -> Dict:
        """Get CPU capabilities."""
        import multiprocessing
        
        return {
            "cores": multiprocessing.cpu_count(),
            "available": True
        }
```

#### **5.2 Hardware Routes**

**server/api/v1/routes/hardware.py:**
```python
from fastapi import APIRouter, Depends
from server.services.hardware_service import HardwareService
from server.api.v1.models.responses import HardwareDetectionResponse

router = APIRouter()


def get_hardware_service():
    """Dependency injection for hardware service."""
    return HardwareService()


@router.get("/hardware/detect", response_model=HardwareDetectionResponse)
async def detect_hardware(
    hardware_service: HardwareService = Depends(get_hardware_service)
):
    """
    Detect all available hardware accelerators.
    
    This endpoint scans for:
    - FPGA devices (Tang Nano 9K via serial)
    - Embedded systems (ELM11 microcontrollers)
    - GPU availability (NVIDIA CUDA)
    - CPU core count
    
    Useful for automated backend selection and troubleshooting.
    """
    results = await hardware_service.detect_all_hardware()
    return results
```

#### **5.3 Benchmark Service**

**server/api/v1/routes/benchmark.py:**
```python
from fastapi import APIRouter, Depends, BackgroundTasks
from server.api.v1.models.requests import BenchmarkRequest
from server.api.v1.models.responses import BenchmarkResponse
from server.services.wavelet_service import WaveletService
import numpy as np
import time
from typing import Dict

router = APIRouter()


@router.post("/benchmark", response_model=BenchmarkResponse)
async def run_benchmark(
    request: BenchmarkRequest,
    background_tasks: BackgroundTasks
):
    """
    Run performance benchmarks across all available backends.
    
    This automates the MVP research questions by testing:
    - pycwt performance characteristics (Question 1)
    - PyWavelets vs pycwt comparison (Question 2)
    - FPGA acceleration benefits (FPGA research)
    
    Parameters:
    - signal_length: Number of timepoints to test
    - mc_count: Monte Carlo iterations
    - backends: List of backends to test (default: all available)
    """
    wavelet_service = WaveletService()
    
    # Generate test signals
    t = np.linspace(0, 10, request.signal_length)
    signal1 = np.sin(2 * np.pi * t)
    signal2 = np.cos(2 * np.pi * t)
    
    results = {}
    
    for backend in request.backends:
        try:
            start = time.time()
            
            result = await wavelet_service.compute_wct(
                signal1=signal1,
                signal2=signal2,
                dt=0.1,
                mc_count=request.mc_count,
                backend=backend
            )
            
            elapsed = time.time() - start
            
            results[backend] = {
                "status": "completed",
                "computation_time": elapsed,
                "speedup": 1.0  # Computed relative to sequential
            }
        
        except Exception as e:
            results[backend] = {
                "status": "failed",
                "error": str(e)
            }
    
    # Calculate speedups relative to sequential
    if "sequential" in results and results["sequential"]["status"] == "completed":
        baseline = results["sequential"]["computation_time"]
        for backend, data in results.items():
            if data["status"] == "completed":
                data["speedup"] = baseline / data["computation_time"]
    
    return {
        "signal_length": request.signal_length,
        "mc_count": request.mc_count,
        "results": results
    }
```

---

### **Phase 6: Job Queue & Batch Processing (Week 6)**

#### **6.1 Job Service with Redis/Celery**

**server/services/job_service.py:**
```python
from celery import Celery
from typing import Dict, List
import uuid
import logging
from server.config import settings

logger = logging.getLogger(__name__)

# Celery app
celery_app = Celery(
    "pycwt_jobs",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)


class JobService:
    """Service for managing batch job processing."""
    
    def __init__(self):
        self.celery = celery_app
    
    async def submit_batch_job(self, tasks: List[Dict]) -> Dict:
        """
        Submit a batch of wavelet analysis tasks.
        
        Returns job ID for tracking.
        """
        job_id = str(uuid.uuid4())
        
        logger.info(f"Submitting batch job {job_id} with {len(tasks)} tasks")
        
        # Queue tasks with Celery
        for i, task in enumerate(tasks):
            process_wavelet_task.apply_async(
                args=[task],
                task_id=f"{job_id}_{i}"
            )
        
        return {
            "job_id": job_id,
            "status": "queued",
            "tasks_count": len(tasks)
        }
    
    async def get_job_status(self, job_id: str) -> Dict:
        """Get status of a batch job."""
        # Query Celery for task status
        # Implementation depends on job tracking strategy
        
        return {
            "job_id": job_id,
            "status": "completed",  # queued, processing, completed, failed
            "progress": 100
        }


@celery_app.task
def process_wavelet_task(task: Dict):
    """Celery task for processing individual wavelet analysis."""
    import numpy as np
    from server.services.wavelet_service import WaveletService
    
    service = WaveletService()
    
    if task["type"] == "wct":
        signal1 = np.array(task["signal1"])
        signal2 = np.array(task["signal2"])
        # Use synchronous version or asyncio.run()
        # result = service.compute_wct(...)
        pass
    
    # Process other task types...
```

---

### **Phase 7: Testing & Documentation (Week 7)**

#### **7.1 Comprehensive Test Suite**

**server/tests/test_wavelet.py:**
```python
import pytest
from fastapi.testclient import TestClient
from server.main import app
import numpy as np

client = TestClient(app)


def test_cwt_basic():
    """Test basic CWT computation."""
    data = np.sin(np.linspace(0, 10, 100)).tolist()
    
    response = client.post("/api/v1/wavelet/cwt", json={
        "data": data,
        "dt": 0.1
    })
    
    assert response.status_code == 200
    result = response.json()
    assert "wave" in result
    assert "computation_time" in result


def test_wct_with_backends():
    """Test WCT with different backends."""
    signal1 = np.sin(np.linspace(0, 10, 50)).tolist()
    signal2 = np.cos(np.linspace(0, 10, 50)).tolist()
    
    backends = ["sequential", "joblib"]
    
    for backend in backends:
        response = client.post("/api/v1/wavelet/wct", json={
            "signal1": signal1,
            "signal2": signal2,
            "dt": 0.1,
            "backend": backend
        })
        
        assert response.status_code == 200
        result = response.json()
        assert result["backend_used"] == backend


def test_invalid_input():
    """Test validation of invalid inputs."""
    response = client.post("/api/v1/wavelet/wct", json={
        "signal1": [1, 2, 3],
        "signal2": [1, 2],  # Different length
        "dt": 0.1
    })
    
    assert response.status_code == 400
```

#### **7.2 Integration Tests**

**server/tests/test_integration.py:**
```python
import pytest
from server.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_full_workflow():
    """Test complete workflow: backend detection → WCT computation."""
    # 1. Check health
    response = client.get("/health")
    assert response.status_code == 200
    
    # 2. List backends
    response = client.get("/api/v1/backends/")
    assert response.status_code == 200
    backends = response.json()["backends"]
    
    # 3. Detect hardware
    response = client.get("/api/v1/hardware/detect")
    assert response.status_code == 200
    
    # 4. Run WCT
    import numpy as np
    signal1 = np.sin(np.linspace(0, 10, 100)).tolist()
    signal2 = np.cos(np.linspace(0, 10, 100)).tolist()
    
    response = client.post("/api/v1/wavelet/wct", json={
        "signal1": signal1,
        "signal2": signal2,
        "dt": 0.1,
        "backend": "sequential"
    })
    
    assert response.status_code == 200
    assert "WCT" in response.json()
```

---

### **Phase 8: Deployment & Production (Week 8)**

#### **8.1 Docker Configuration**

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements-server.txt .
RUN pip install --no-cache-dir -r requirements-server.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run server
CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis
    volumes:
      - ./server:/app/server
    devices:
      - /dev/ttyUSB0:/dev/ttyUSB0  # FPGA device
    privileged: true
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
  
  celery_worker:
    build: .
    command: celery -A server.services.job_service:celery_app worker --loglevel=info
    environment:
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis
    volumes:
      - ./server:/app/server
```

---

## 🎯 Success Metrics

### **Performance Targets:**
- ✅ API response time <100ms for backend listing
- ✅ WCT computation time matches direct pycwt usage (minimal overhead)
- ✅ WebSocket latency <50ms for streaming
- ✅ Support 10+ concurrent requests

### **Reliability Targets:**
- ✅ 99% uptime for API server
- ✅ Graceful fallback when hardware unavailable
- ✅ Comprehensive error messages
- ✅ 80%+ test coverage

### **Documentation Targets:**
- ✅ Complete OpenAPI/Swagger documentation
- ✅ Client library examples (Python, JS, R, MATLAB)
- ✅ Deployment guide (Docker, bare metal)
- ✅ Troubleshooting guide

---

## 🔗 Integration with Research Documents

### **Enables MVP Research (wavelets-deep-research-prompt2-mvp.md):**
```python
# Question 1: pycwt Performance Characterization
for n in [100, 1000, 10000, 100000]:
    response = requests.post("/api/v1/benchmark", json={
        "signal_length": n,
        "mc_count": 300,
        "backends": ["sequential"]
    })
    print(f"N={n}: {response.json()['results']['sequential']['computation_time']}s")
```

### **Enables FPGA Research:**
```python
# Real-time latency testing
import websocket

ws = websocket.WebSocket()
ws.connect("ws://localhost:8000/ws/stream/wct")
ws.send(json.dumps({"type": "config", "dt": 0.001, "backend": "elm11"}))

# Send EEG chunks, measure response time
```

### **Enables Comparative Analysis:**
```python
# Compare all backends automatically
response = requests.post("/api/v1/benchmark", json={
    "signal_length": 10000,
    "backends": ["sequential", "joblib", "elm11"],
    "mc_count": 300
})

for backend, data in response.json()["results"].items():
    print(f"{backend}: {data['speedup']:.2f}× speedup")
```

---

## ⚠️ Risk Mitigation

### **Technical Risks:**

| Risk | Impact | Mitigation |
|------|--------|------------|
| Hardware detection fails | High | Graceful fallback, clear error messages |
| FPGA driver issues | Medium | Comprehensive detection script, troubleshooting docs |
| NumPy serialization issues | Medium | Custom JSON encoders for complex/numpy types |
| Async overhead | Low | Benchmark against direct pycwt usage |

### **Operational Risks:**

| Risk | Impact | Mitigation |
|------|--------|------------|
| Concurrent job overload | High | Redis queue with max workers limit |
| Memory exhaustion | High | Input validation (max array size) |
| WebSocket connection leaks | Medium | Connection timeout, cleanup on disconnect |

---

## 📚 Documentation Deliverables

1. **API Reference** - Auto-generated from FastAPI (Swagger UI)
2. **Integration Guide** - How to use from Python/JS/R/MATLAB
3. **Deployment Guide** - Docker, systemd, production config
4. **Performance Guide** - Backend selection, optimization tips
5. **Troubleshooting Guide** - Common issues and solutions

---

## 🚀 Future Enhancements (Post v1.0)

1. **Authentication & Authorization**
   - API key management
   - JWT tokens for user sessions
   - Rate limiting per user

2. **Advanced Features**
   - Multi-dimensional array support (3D wavelet transforms)
   - Custom wavelet definitions via API
   - Result caching for repeated queries

3. **Monitoring & Analytics**
   - Prometheus metrics endpoint
   - Grafana dashboard
   - Usage analytics

4. **Additional Backends**
   - GPU acceleration (CUDA)
   - Distributed processing (Dask clusters)
   - Cloud backend (AWS Lambda)

---

## 🎓 Conclusion

This implementation plan provides a complete roadmap from the API specification to a production-ready REST API that:

- ✅ Exposes all pycwt-mod capabilities via HTTP/WebSocket
- ✅ Supports hardware acceleration (FPGA, embedded, GPU future)
- ✅ Enables research validation (MVP, FPGA, Phase 2)
- ✅ Provides client libraries for multiple languages
- ✅ Includes comprehensive testing and documentation
- ✅ Ready for Docker deployment

**Estimated Total Effort:** 6-8 weeks for single developer  
**Priority:** High (enables external integration and research validation)  
**Next Step:** Phase 1 implementation (Core API Infrastructure)
