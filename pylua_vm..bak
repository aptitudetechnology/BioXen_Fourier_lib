import subprocess
import threading
import queue
import socket
import os

class LuaVM:
    def __init__(self, name):
        self.name = name
        self.process = None
        self.stdout_queue = queue.Queue()
        self.stderr_queue = queue.Queue()
        self.server_thread = None
        self.client_socket = None
        self.server_socket = None
        self.running = False

    def execute(self, lua_code):
        """Execute Lua code and return the result (stdout)."""
        command = ["lua", "-e", lua_code]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            raise RuntimeError(result.stderr.strip())

    def start_server(self, port=8080):
        """Start a Lua socket server on the given port."""
        def server():
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(("", port))
            self.server_socket.listen(1)
            self.running = True
            while self.running:
                client, addr = self.server_socket.accept()
                data = client.recv(1024)
                if data:
                    self.stdout_queue.put(data.decode())
                client.close()
        self.server_thread = threading.Thread(target=server, daemon=True)
        self.server_thread.start()

    def connect_to(self, host, port):
        """Connect to another VM's server."""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

    def send_message(self, message):
        """Send a message to the connected server."""
        if self.client_socket:
            self.client_socket.sendall(message.encode())

    def receive_message(self):
        """Receive a message from the server (blocking)."""
        try:
            return self.stdout_queue.get(timeout=10)
        except queue.Empty:
            return None

    def shutdown(self):
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        if self.client_socket:
            self.client_socket.close()
        if self.server_thread:
            self.server_thread.join(timeout=1)

class VMManager:
    def __init__(self):
        self.vms = {}

    def create_vm(self, name):
        vm = LuaVM(name)
        self.vms[name] = vm
        return vm

    def shutdown_all(self):
        for vm in self.vms.values():
            vm.shutdown()
        self.vms.clear()
