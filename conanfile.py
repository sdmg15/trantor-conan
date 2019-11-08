import os 
from conans import ConanFile, CMake, tools

class TrantorConan(ConanFile):
    name = "trantor"
    version = "1.0.0-rc6"
    license = "MIT"
    author = "Tao An"
    url = "https://github.com/sdmg15/trantor-conan"
    homepage = "https://github.com/an-tao/trantor"
    description = "A non-blocking I/O based TCP network library"
    topics = ("io", "tcp", "network")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = "cmake"
    exports_sources = "CMakeLists.txt"
    requires = ("openssl/1.0.2t", "c-ares/1.15.0")

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"
    
    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        sha256 = "7eebdec4cac40179166ffb2e859d39be0aab1acb20827dd61cca0bb0f7bea751"
        tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage, self.version), sha256=sha256)
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("License", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")