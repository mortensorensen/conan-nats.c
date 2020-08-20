from conans import ConanFile, CMake, tools
import os
import re


class NatsCConan(ConanFile):
    name = "nats.c"
    version = "2.1.0"
    description = "A C client for the NATS messaging system"
    topics = ("conan", "nats.c", "communication", "messaging", "protocols")
    url = "https://github.com/mortensorensen/conan-nats.c"
    homepage = "https://github.com/nats-io/nats.c"
    license = "https://github.com/nats-io/nats.c/blob/master/LICENSE"
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "no_spin": [True, False],
        "tls": [True, False],
        "tls_force_host_verify": [True, False],
        "tls_use_openssl_1_1_api": [True, False],
    }
    default_options = {
        "shared": False,
        "no_spin": False,
        "tls": True,
        "tls_force_host_verify": True,
        "tls_use_openssl_1_1_api": True,
    }
    _source_subfolder = "source_subfolder"
    requires = "protobuf-c/1.3.2@mortensoerensen+conan-protobuf-c/stable"

    def source(self):
        sha256 = "1493ae3d790e2ebc4d77c65ef2957e2fb77182d69afeeeb2be1e1e6bee0ca12e"
        tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage, self.version), sha256=sha256)
        extracted_dir = "-".join([self.name, self.version])
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["NATS_BUILD_NO_SPIN"] = self.options.no_spin
        cmake.definitions["NATS_BUILD_WITH_TLS"] = self.options.tls
        cmake.definitions["NATS_BUILD_TLS_FORCE_HOST_VERIFY"] = self.options.tls_force_host_verify
        cmake.definitions["NATS_BUILD_TLS_USE_OPENSSL_1_1_API"] = self.options.tls_use_openssl_1_1_api
        cmake.definitions["CMAKE_MACOSX_RPATH"] = True
        cmake.configure()
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", src=self._source_subfolder, dst="licenses")
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
