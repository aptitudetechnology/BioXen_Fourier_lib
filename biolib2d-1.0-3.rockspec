package = "biolib2d"
version = "1.0-3"
source = {
   url = "git://github.com/aptitudetechnology/BioLib2D",
   tag = "v1.0-3"
}
description = {
   summary = "Love2D-based visualization library for cellular, genetic, and protein processes",
   detailed = "BioLib2D is a Love2D-based visualization library specifically designed for rendering cellular, genetic, and protein processes using real-time data from BioXen virtual machines.",
   homepage = "https://github.com/aptitudetechnology/BioLib2D",
   license = "MIT"
}
dependencies = {
   "lua >= 5.1"
}
build = {
   type = "builtin",
   modules = {
      biolib2d = "init.lua",
      ["biolib2d.main"] = "main.lua",
      ["biolib2d.conf"] = "conf.lua",
      ["biolib2d.core"] = "src/BioLib2D.lua",
      ["biolib2d.components.ATPSystem"] = "src/components/ATPSystem.lua",
      ["biolib2d.components.VMCell"] = "src/components/VMCell.lua",
      ["biolib2d.components.BioXenConnector"] = "src/components/BioXenConnector.lua",
      ["biolib2d.components.GeneticCircuit"] = "src/components/GeneticCircuit.lua",
      ["biolib2d.utils.export"] = "src/utils/export.lua",
      ["biolib2d.utils.colors"] = "src/utils/colors.lua"
   },
   copy_directories = {
      "data"
   }
}
