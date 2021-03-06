# This spec file is based on other spec files (for compatiblity) PKGBUILDs and EBUILDs available from
#  [1] https://www.archlinux.org/packages/extra/x86_64/chromium/
#  [2] https://packages.gentoo.org/packages/www-client/chromium
#  [3] https://build.opensuse.org/package/show/openSUSE:Factory/chromium
#  [4] https://pkgs.fedoraproject.org/cgit/rpms/chromium.git 
#  [5] http://copr-dist-git.fedorainfracloud.org/cgit/lantw44/chromium/chromium.git
#  [6] https://anonscm.debian.org/cgit/pkg-chromium/pkg-chromium.git/tree/debian
#  [7] http://www.linuxfromscratch.org/blfs/view/cvs/xsoft/chromium.html
#  [8] https://aur.archlinux.org/packages/chromium-gtk2/
#  [9] https://github.com/RussianFedora/chromium/


%global chromiumdir %{_libdir}/chromium
%global crd_path %{_libdir}/chrome-remote-desktop
# Do not check any ffmpeg or libmedia bundle files in libdir for requires
%global __requires_exclude_from ^%{chromiumdir}/libffmpeg.*$
%global __requires_exclude_from ^%{chromiumdir}/libmedia.*$

# Generally chromium is a monster if you compile the source code, enabling all; and takes hours compiling; common users doesn't need all tools.
%bcond_without devel_tools
# Chromium users doesn't need chrome-remote-desktop
%bcond_without remote_desktop
#
# Get the version number of latest stable version
# $ curl -s 'https://omahaproxy.appspot.com/all?os=linux&channel=stable' | sed 1d | cut -d , -f 3
%bcond_without normalsource

%if 0%{?fedora} >= 27
%global debug_package %{nil}
%endif

# Use clang compiler (downloaded binaries from google). Results in faster build and smaller chromium.
%if 0
%bcond_without clang
%else
%bcond_with clang
%endif

%if 0%{?fedora} < 26
%bcond_without system_jinja2
%else
%bcond_with system_jinja2
%endif

# markupsafe
%bcond_with system_markupsafe


# https://github.com/dabeaz/ply/issues/66
%if 0%{?fedora} >= 24
%bcond_without system_ply
%else
%bcond_with system_ply
%endif

# Require libxml2 > 2.9.4 for XML_PARSE_NOXXE
%if 0
%bcond_without system_libxml2
%else
%bcond_with system_libxml2
%endif

# Require harfbuzz >= 1.4.2 for hb_variation_t
%if 0%{?fedora} >= 26
%bcond_without system_harfbuzz
%else
%bcond_with system_harfbuzz
%endif

# Allow building with symbols to ease debugging
%bcond_with symbol

# Allow disabling unconditional build dependency on clang
%bcond_without require_clang

# Chromium breaks on wayland, hidpi, and colors with gtk3 enabled.
%bcond_with _gkt3

Name:       chromium-freeworld
Version:    60.0.3112.101
Release:    2%{?dist}
Summary:    An open-source project that aims to build a safer, faster, and more stable browser

Group:      Applications/Internet
License:    BSD and LGPLv2+
URL:        https://www.chromium.org
Vendor:     URPMS

%if %{with normalsource}
Source0:    https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%{version}.tar.xz
%endif
Source1:    chromium-latest.py
Source2:    chromium-ffmpeg-clean.sh
Source3:    chromium-ffmpeg-free-sources.py
%if %{with remote_desktop}
Source33:   chrome-remote-desktop.service
%endif
Source997:  https://github.com/UnitedRPMs/chromium-freeworld/raw/master/depot_tools.tar.xz
Source998:  https://github.com/UnitedRPMs/chromium-freeworld/raw/master/gn-binaries.tar.xz

# The following two source files are copied and modified from
# https://repos.fedorapeople.org/repos/spot/chromium/
Source10:   chromium-wrapper.txt
Source11:   chromium-freeworld.desktop

# The following two source files are copied verbatim from
# http://pkgs.fedoraproject.org/cgit/rpms/chromium.git/tree/
Source12:   chromium-freeworld.xml
Source13:   chromium-freeworld.appdata.xml

# Reverse https://chromium.googlesource.com/chromium/src/+/8d1845c2267b05df565fa33e3c5e2b0e242a21cc%5E%21/
Patch0:     issue2961473002_1_10001.diff

# Add a patch from Fedora to fix GN build
# http://pkgs.fedoraproject.org/cgit/rpms/chromium.git/commit/?id=0df9641
Patch1:     chromium-60.0.3112.7-last-commit-position.patch
# Add several patches from Fedora to fix build with GCC 7
Patch5:     chromium-60.0.3095.5-gcc7.patch
Patch9:     chromium-56.0.2924.87-fpermissive.patch
# Fixes from Gentoo
Patch7:     chromium-gn-bootstrap-r8.patch
Patch8:     chromium-FORTIFY_SOURCE-r1.patch

# Change struct ucontext to ucontext_t in breakpad
# https://patchwork.openembedded.org/patch/141358/
Patch10:    chromium-59.0.3071.115-ucontext-fix.patch


ExclusiveArch: i686 x86_64 armv7l

# Make sure we don't encounter GCC 5.1 bug
%if 0%{?fedora} >= 22
BuildRequires: gcc >= 5.1.1-2
%endif

%if %{with clang} || %{with require_clang} 
BuildRequires: clang
%endif
# Basic tools and libraries
BuildRequires: ninja-build, bison, gperf, hwdata
BuildRequires: libgcc(x86-32), glibc(x86-32), libatomic
BuildRequires: libcap-devel, cups-devel, minizip-devel, alsa-lib-devel
BuildRequires: pkgconfig(gtk+-2.0), pkgconfig(libexif), pkgconfig(nss)
BuildRequires: pkgconfig(xtst), pkgconfig(xscrnsaver)
BuildRequires: pkgconfig(dbus-1), pkgconfig(libudev)
BuildRequires: pkgconfig(gnome-keyring-1)
BuildRequires: pkgconfig(libffi)
# remove_bundled_libraries.py --do-remove
BuildRequires: python2-rpm-macros
BuildRequires: python-beautifulsoup4
BuildRequires: python-html5lib
%if %{with system_jinja2}
%if 0%{?fedora} >= 24
BuildRequires: python2-jinja2
%else
BuildRequires: python-jinja2
%endif
%endif

%if %{with system_markupsafe}
%if 0%{?fedora} >= 26
BuildRequires: python2-markupsafe
%else
BuildRequires: python-markupsafe
%endif
%endif

%if %{with system_ply}
BuildRequires: python2-ply
%endif
# replace_gn_files.py --system-libraries
BuildRequires: flac-devel
# replace_gn_files.py --system-libraries
BuildRequires: flac-devel
%if %{with system_harfbuzz}
BuildRequires: harfbuzz-devel
%endif
BuildRequires: libjpeg-turbo-devel
BuildRequires: libpng-devel
BuildRequires: libwebp-devel
BuildRequires: pkgconfig(libxslt)
%if %{with system_libxml2}
BuildRequires: pkgconfig(libxml-2.0)
%endif
BuildRequires: re2-devel
BuildRequires: snappy-devel
BuildRequires: yasm
BuildRequires: zlib-devel
# use_*
BuildRequires: pciutils-devel
BuildRequires: speech-dispatcher-devel
BuildRequires: pulseaudio-libs-devel
# Only for non-normal source
BuildRequires: wget
# install desktop files
BuildRequires: desktop-file-utils
# install AppData files
BuildRequires: libappstream-glib
# remote desktop needs this
BuildRequires: pam-devel
BuildRequires: systemd
# CLANG
%if 0%{?clang}
BuildRequires: clang
%endif
# GTK3
BuildRequires: pkgconfig(gtk+-3.0) 
# markupsafe missed
BuildRequires: git
BuildRequires: nodejs
BuildRequires: libdrm-devel
BuildRequires: mesa-libGL-devel
# vulcan
BuildRequires: vulkan-devel
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
Requires: hicolor-icon-theme
Requires: re2
Requires: %{name}-libs = %{version}-%{release}

%if 0%{?fedora}
# This enables support for u2f tokens
Recommends: u2f-hidraw-policy
%endif

Provides: chromium >= 54
Recommends: chromium-pepper-flash
Recommends: chromium-widevine

%description
Chromium is a browser that combines a minimal design with sophisticated
technology to make the web faster, safer, and easier.

This is the stable channel Chromium browser. It offers a rock solid
browser which is updated with features and fixes once they have been
thoroughly tested. If you want the latest features, install the
chromium-unstable package instead.

Note: If you are reverting from unstable to stable or beta channel, you may
experience tab crashes on startup. This crash only affects tabs restored
during the first launch due to a change in how tab state is stored.
See http://bugs.chromium.org/34688. It's always a good idea to back up
your profile before changing channels.

%package libs
Summary: Shared libraries used by chromium (and chrome-remote-desktop)
Requires: %{name}-libs-media%{_isa} = %{version}-%{release}
Provides: %{name}-libs%{_isa} = %{version}-%{release}
Provides: chromium-libs >= 54

%description libs
Shared libraries used by chromium (and chrome-remote-desktop).

%if %{with devel_tools}
%package chromedriver
Summary: WebDriver for Google Chrome/Chromium
Group: Development/Libraries
Provides: chromedriver >= 54

%description chromedriver
WebDriver is an open source tool for automated testing of webapps across many
browsers. It provides capabilities for navigating to web pages, user input,
JavaScript execution, and more. ChromeDriver is a standalone server which
implements WebDriver's wire protocol for Chromium. It is being developed by
members of the Chromium and WebDriver teams.
%endif

%package libs-media
Summary: Chromium media libraries built with all possible codecs
Provides: %{name}-libs-media%{_isa} = %{version}-%{release}
Provides: libffmpeg.so()(64bit)
Provides: chromium-libs-media-freeworld >= 54
Provides: chromium-libs-media >= 54

%description libs-media
Chromium media libraries built with all possible codecs. Chromium is an
open-source web browser, powered by WebKit (Blink). This package replaces
the default chromium-libs-media package, which is limited in what it
can include.

%if %{with remote_desktop}
%package -n chrome-remote-desktop
Summary: Remote desktop support for google-chrome & chromium
Requires(pre): shadow-utils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Requires: xorg-x11-server-Xvfb

Requires: %{name}-libs%{_isa} = %{version}-%{release}

%description -n chrome-remote-desktop
Remote desktop support for google-chrome & chromium.
%endif

%prep
%if %{with normalsource}
%setup -n chromium-%{version} 
%else
wget -c https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%{version}.tar.xz
tar xJf %{_builddir}/chromium-%{version}.tar.xz -C %{_builddir}
%setup -T -D -n chromium-%{version}
%endif

patch -Rp1 -i %{_sourcedir}/issue2961473002_1_10001.diff
%patch1 -p1 -b .lastcommit
%patch5 -p1 -b .gcc7
%patch7 -p1 -b .gn-bootstrap-r8
%patch8 -p1
%patch9 -p1 -b .permissive
%if 0%{?fedora} >= 27
%patch10 -p1 -b .ucontextfix
%endif

tar xJf %{S:998} -C %{_builddir}
tar xJf %{S:997} -C %{_builddir}

%if %{with normalsource}
pushd third_party
rm -rf markupsafe/
git clone --depth 1 https://github.com/pallets/markupsafe.git 
cp -f $PWD/markupsafe/markupsafe/*.py $PWD/markupsafe/
cp -f $PWD/markupsafe/markupsafe/*.c $PWD/markupsafe/
popd
%endif

# node fix
mkdir -p third_party/node/linux/node-linux-x64/bin
ln -s /usr/bin/node third_party/node/linux/node-linux-x64/bin/node

%if %{with remote_desktop}
# Fix hardcoded path in remoting code
sed -i 's|/opt/google/chrome-remote-desktop|%{crd_path}|g' remoting/host/setup/daemon_controller_delegate_linux.cc
%endif

# https://groups.google.com/a/chromium.org/d/msg/chromium-packagers/wuInaKJkosg/kMfIV_7wDgAJ
rm -rf third_party/freetype/src
git clone https://chromium.googlesource.com/chromium/src/third_party/freetype2 third_party/freetype/src


### build with widevine support

# Patch from crbug (chromium bugtracker)
# fix the missing define (if not, fail build) (need upstream fix) (https://crbug.com/473866)
sed '14i#define WIDEVINE_CDM_VERSION_STRING "Something fresh"' -i "third_party/widevine/cdm/stub/widevine_cdm_version.h"

./build/linux/unbundle/remove_bundled_libraries.py --do-remove \
    base/third_party/dmg_fp \
    base/third_party/dynamic_annotations \
    base/third_party/icu \
    base/third_party/libevent \
    base/third_party/nspr \
    base/third_party/superfasthash \
    base/third_party/symbolize \
    base/third_party/valgrind \
    base/third_party/xdg_mime \
    base/third_party/xdg_user_dirs \
breakpad/src/third_party/curl \
    chrome/third_party/mozilla_security_manager \
    courgette/third_party \
native_client/src/third_party/dlmalloc \
native_client/src/third_party/valgrind \
    net/third_party/mozilla_security_manager \
    net/third_party/nss \
    third_party/node \
third_party/node/node_modules/vulcanize/third_party/UglifyJS2 \
    third_party/adobe \
    third_party/analytics \
third_party/angle \
    third_party/markupsafe \
third_party/angle/src/common/third_party/numerics \
third_party/angle/src/third_party/compiler \
third_party/angle/src/third_party/libXNVCtrl \
third_party/angle/src/third_party/murmurhash \
third_party/angle/src/third_party/trace_event \
    third_party/boringssl \
    third_party/brotli \
    third_party/cacheinvalidation \
third_party/catapult \
third_party/catapult/third_party/polymer \
third_party/catapult/third_party/py_vulcanize \
third_party/catapult/third_party/py_vulcanize/third_party/rcssmin \
third_party/catapult/third_party/py_vulcanize/third_party/rjsmin \
third_party/catapult/tracing/third_party/d3 \
third_party/catapult/tracing/third_party/gl-matrix \
third_party/catapult/tracing/third_party/jszip \
third_party/catapult/tracing/third_party/mannwhitneyu \
    third_party/ced \
    third_party/cld_2 \
    third_party/cld_3 \
third_party/cros_system_api \
    third_party/devscripts \
    third_party/dom_distiller_js \
third_party/ffmpeg \
    third_party/fips181 \
    third_party/flatbuffers \
    third_party/flot \
    third_party/google_input_tools \
    third_party/google_input_tools/third_party/closure_library \
    third_party/google_input_tools/third_party/closure_library/third_party/closure \
    third_party/hunspell \
    third_party/iccjpeg \
    third_party/icu \
%if !%{with system_jinja2}
    third_party/jinja2 \
%endif
    third_party/jstemplate \
    third_party/khronos \
    third_party/leveldatabase \
    third_party/libaddressinput \
    third_party/libjingle \
    third_party/libphonenumber \
    third_party/libsecret \
third_party/libsrtp \
    third_party/libudev \
    third_party/libusb \
    third_party/libvpx \
    third_party/libvpx/source/libvpx/third_party/googletest \
    third_party/libvpx/source/libvpx/third_party/libwebm \
    third_party/libvpx/source/libvpx/third_party/libyuv \
    third_party/libvpx/source/libvpx/third_party/x86inc \
    third_party/libwebm \
%if %{with system_libxml2}
    third_party/libxml/chromium \
%else
    third_party/libxml \
%endif
    third_party/libXNVCtrl \
third_party/libyuv \
third_party/lss \
    third_party/lzma_sdk \
    third_party/mesa \
    third_party/modp_b64 \
    third_party/mt19937ar \
    third_party/openh264 \
third_party/openmax_dl \
    third_party/opus \
    third_party/ots \
third_party/freetype \
%if !%{with system_ply}
    third_party/ply \
%endif
    third_party/polymer \
    third_party/protobuf \
    third_party/protobuf/third_party/six \
    third_party/qcms \
    third_party/sfntly \
third_party/skia \
    third_party/smhasher \
    third_party/speech-dispatcher \
    third_party/sqlite \
    third_party/expat \
    third_party/tcmalloc \
    third_party/usb_ids \
    third_party/usrsctp \
    third_party/web-animations-js \
    third_party/webdriver \
    third_party/WebKit \
    third_party/webrtc \
    third_party/widevine \
    third_party/inspector_protocol \
v8/third_party/inspector_protocol \
    third_party/woff2 \
third_party/xdg-utils \
    third_party/yasm/run_yasm.py \
    third_party/zlib/google \
    third_party/sinonjs \
    third_party/blanketjs \
    third_party/qunit \
    url/third_party/mozilla \
    third_party/swiftshader \
    third_party/swiftshader/third_party/llvm-subzero \
    third_party/swiftshader/third_party/subzero \
    third_party/pdfium \
    third_party/pdfium/third_party/agg23 \
    third_party/pdfium/third_party/base \
    third_party/pdfium/third_party/bigint \
    third_party/pdfium/third_party/build \
    third_party/pdfium/third_party/freetype \
    third_party/pdfium/third_party/lcms2-2.6 \
    third_party/pdfium/third_party/libopenjpeg20 \
    third_party/pdfium/third_party/libpng16 \
    third_party/pdfium/third_party/libtiff \
    third_party/googletest \
    third_party/glslang-angle \
    third_party/vulkan-validation-layers \
    third_party/spirv-tools-angle \
    third_party/spirv-headers \
    third_party/catapult/tracing/third_party/oboe \
%if !%{with system_harfbuzz}
    third_party/harfbuzz-ng \
%endif
v8/src/third_party/valgrind 

./build/linux/unbundle/replace_gn_files.py --system-libraries \
    flac \
    libdrm \
%if %{with system_harfbuzz}
    harfbuzz-ng \
%endif
    libjpeg \
    libpng \
    libwebp \
%if %{with system_libxml2}
    libxml \
%endif
    libxslt \
    re2 \
    snappy \
    yasm \
    zlib

./build/download_nacl_toolchains.py --packages \
    nacl_x86_glibc,nacl_x86_newlib,pnacl_newlib,pnacl_translator sync --extract

sed -i "s|'ninja'|'ninja-build'|" tools/gn/bootstrap/bootstrap.py
sed -i 's|//third_party/usb_ids|/usr/share/hwdata|g' device/usb/BUILD.gn

%if %{with system_jinja2}
rmdir third_party/jinja2 
ln -s %{python2_sitelib}/jinja2 third_party/jinja2
%endif

%if %{with system_markupsafe}
rmdir third_party/markupsafe && mkdir -p third_party/markupsafe
ln -s %{python2_sitearch}/markupsafe third_party/markupsafe
%endif

%if %{with system_ply}
rmdir third_party/ply
ln -s %{python2_sitelib}/ply third_party/ply
%endif

mkdir -p native_client/toolchain/.tars/linux_x86
touch native_client/toolchain/.tars/linux_x86/pnacl_translator.json

pushd native_client/toolchain
ln -s ../../out/Release/gen/sdk/linux_x86 linux_x86
popd

mkdir -p third_party/llvm-build/Release+Asserts/bin
pushd third_party/llvm-build/Release+Asserts/bin
ln -s /usr/bin/clang clang
popd


%build
cd %{_builddir}/chromium-%{version}/

%if %{with clang}
export CC=clang CXX=clang++
CXXFLAGS+="-Wno-expansion-to-defined -fno-delete-null-pointer-checks"
CFLAGS+="-Wno-expansion-to-defined -fno-delete-null-pointer-checks"
%endif


_flags+=(
    'is_debug=false'
%if 0%{?clang}
    'is_clang=true' 
    'clang_base_path="/usr"'
    'clang_use_chrome_plugins=false'
%else
    'is_clang=false' 
%endif
    'fatal_linker_warnings=false'
    'treat_warnings_as_errors=false'
    'fieldtrial_testing_like_official_build=true'
    'remove_webcore_debug_symbols=true'
    'ffmpeg_branding="Chrome"'
    'proprietary_codecs=true'
    'link_pulseaudio=true'
    'linux_use_bundled_binutils=false'
    'use_allocator="none"'
    'use_cups=true'
    'use_gconf=false'
    'use_gnome_keyring=false'
    'use_gold=false'
    'use_kerberos=true'
    'use_pulseaudio=true'
    'use_sysroot=false'
    'enable_hangout_services_extension=true'
    'enable_widevine=true'
    'enable_nacl=false'
    'enable_nacl_nonsfi=false'
    "google_api_key=\"AIzaSyD1hTe85_a14kr1Ks8T3Ce75rvbR1_Dx7Q\""
    "google_default_client_id=\"4139804441.apps.googleusercontent.com\""
    "google_default_client_secret=\"KDTRKEZk2jwT_7CDpcmMA--P\""
%ifarch x86_64
    'system_libdir="lib64"'
%endif
    'is_component_ffmpeg=true' 
    'is_component_build=false'
    'symbol_level=0'
    'remove_webcore_debug_symbols=true'
%if %{with _gtk3}
    'use_gtk3=true'
%else
    'use_gtk3=false'
%endif
)

if tc-is-cross-compiler; then
		local -x AR=${BUILD_AR}
		local -x CC=${BUILD_CC}
		local -x CXX=${BUILD_CXX}
		local -x NM=${BUILD_NM}
		local -x CFLAGS=${BUILD_CFLAGS}
		local -x CXXFLAGS=${BUILD_CXXFLAGS}
		local -x LDFLAGS=${BUILD_LDFLAGS}
	fi

export PATH=%{_builddir}/tools/depot_tools/:"$PATH"

./tools/gn/bootstrap/bootstrap.py -v --gn-gen-args "${_flags[*]}"


./out/Release/gn gen --args="${_flags[*]}" out/Release 

# SUPER POWER!
jobs=$(grep processor /proc/cpuinfo | tail -1 | grep -o '[0-9]*')

%if %{with devel_tools}
%if 0%{?ninja_build:1}
echo 'first attemp'
ninja-build -C out/Release chrome chrome_sandbox chromedriver widevinecdmadapter -j$jobs
%else
echo 'second attemp'
ninja-build %{_smp_mflags} -C out/Release chrome chrome_sandbox chromedriver widevinecdmadapter -j$jobs
%endif
%else
%if 0%{?ninja_build:1}
echo 'first attemp'
ninja-build -C out/Release chrome widevinecdmadapter -j$jobs
%else
echo 'second attemp'
ninja-build %{_smp_mflags} -C out/Release chrome widevinecdmadapter -j$jobs
%endif
 %endif

%if %{with remote_desktop}
ninja-build -C out/Release remoting_all -j$jobs
%endif

%install

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{chromiumdir}/locales
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_datadir}/appdata
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/gnome-control-center/default-apps
sed -e "s|@LIBDIR@|%{_libdir}|" -e "s|@@BUILDTARGET@@|`cat /etc/redhat-release`|" \
    %{SOURCE10} > chromium-wrapper
install -m 755 chromium-wrapper %{buildroot}%{_bindir}/%{name}
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE11}
install -m 644 %{SOURCE12} %{buildroot}%{_datadir}/gnome-control-center/default-apps/
appstream-util validate-relax --nonet %{SOURCE13}
install -m 644 %{SOURCE13} %{buildroot}%{_datadir}/appdata/
install -m 644 out/Release/chrome.1 %{buildroot}%{_mandir}/man1/%{name}.1
install -m 755 out/Release/chrome %{buildroot}%{chromiumdir}/chromium

%if %{with devel_tools}
install -m 4755 out/Release/chrome_sandbox %{buildroot}%{chromiumdir}/chrome-sandbox
install -m 755 out/Release/chromedriver %{buildroot}%{chromiumdir}/
ln -s %{chromiumdir}/chromedriver %{buildroot}%{_bindir}/%{name}-chromedriver
%endif

# libicu
install -m 644 out/Release/icudtl.dat %{buildroot}%{chromiumdir}/

# nacl
#install -m 755 out/Release/nacl_helper %{buildroot}%{chromiumdir}/
#install -m 755 out/Release/nacl_helper_bootstrap %{buildroot}%{chromiumdir}/
#install -m 644 out/Release/nacl_irt_x86_64.nexe %{buildroot}%{chromiumdir}/

install -m 644 out/Release/natives_blob.bin %{buildroot}%{chromiumdir}/
install -m 644 out/Release/snapshot_blob.bin %{buildroot}%{chromiumdir}/
install -m 644 out/Release/*.pak %{buildroot}%{chromiumdir}/
install -m 644 out/Release/*.so %{buildroot}%{chromiumdir}/
install -m 644 out/Release/locales/*.pak %{buildroot}%{chromiumdir}/locales/
for i in 16 32; do
    mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps
    install -m 644 chrome/app/theme/default_100_percent/chromium/product_logo_$i.png \
        %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/chromium.png
done
for i in 22 24 32 48 64 128 256; do
    if [ ${i} = 32 ]; then ext=xpm; else ext=png; fi
    if [ ${i} = 32 ]; then dir=linux/; else dir=; fi
    mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps
    install -m 644 chrome/app/theme/chromium/${dir}product_logo_$i.${ext} \
        %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/chromium.${ext}
done

mkdir -p %{buildroot}/%{chromiumdir}/PepperFlash

%if %{with remote_desktop}
# Remote desktop bits
mkdir -p %{buildroot}%{crd_path}

pushd %{buildroot}%{crd_path}
ln -s %{_libdir}/%{name} lib
popd

# See remoting/host/installer/linux/Makefile for logic
cp -a out/Release/remoting_native_messaging_host %{buildroot}%{crd_path}/remoting_native_messaging_host
cp -a out/Release/remote_assistance_host %{buildroot}%{crd_path}/remote-assistance-host
cp -a out/Release/remoting_locales %{buildroot}%{crd_path}/
cp -a out/Release/remoting_me2me_host %{buildroot}%{crd_path}/chrome-remote-desktop-host
cp -a out/Release/remoting_start_host %{buildroot}%{crd_path}/start-host

# chromium
mkdir -p %{buildroot}%{_sysconfdir}/chromium/remoting_native_messaging_host
# google-chrome
mkdir -p %{buildroot}%{_sysconfdir}/opt/chrome/
cp -a out/Release/remoting/* %{buildroot}%{_sysconfdir}/chromium/remoting_native_messaging_host/
for i in %{buildroot}%{_sysconfdir}/chromium/remoting_native_messaging_host/*.json; do
    sed -i 's|/opt/google/chrome-remote-desktop|%{crd_path}|g' $i
done
pushd %{buildroot}%{_sysconfdir}/opt/chrome/
ln -s ../../chromium/remoting_native_messaging_host remoting_native_messaging_host
popd

mkdir -p %{buildroot}/var/lib/chrome-remote-desktop
touch %{buildroot}/var/lib/chrome-remote-desktop/hashes

mkdir -p %{buildroot}%{_sysconfdir}/pam.d/
pushd %{buildroot}%{_sysconfdir}/pam.d/
ln -s system-auth chrome-remote-desktop
popd

cp -a remoting/host/linux/linux_me2me_host.py %{buildroot}%{crd_path}/chrome-remote-desktop
cp -a remoting/host/installer/linux/is-remoting-session %{buildroot}%{crd_path}/

mkdir -p %{buildroot}%{_unitdir}
cp -a %{SOURCE33} %{buildroot}%{_unitdir}/
sed -i 's|@@CRD_PATH@@|%{crd_path}|g' %{buildroot}%{_unitdir}/chrome-remote-desktop.service
%endif

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%if %{with remote_desktop}
%pre -n chrome-remote-desktop
getent group chrome-remote-desktop >/dev/null || groupadd -r chrome-remote-desktop

%post -n chrome-remote-desktop
%systemd_post chrome-remote-desktop.service

%preun -n chrome-remote-desktop
%systemd_preun chrome-remote-desktop.service

%postun -n chrome-remote-desktop
%systemd_postun_with_restart chrome-remote-desktop.service
%endif

%files
%license LICENSE
%doc AUTHORS
%{_bindir}/%{name}
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/gnome-control-center/default-apps/%{name}.xml
%{_datadir}/icons/hicolor/16x16/apps/chromium.png
%{_datadir}/icons/hicolor/22x22/apps/chromium.png
%{_datadir}/icons/hicolor/24x24/apps/chromium.png
%{_datadir}/icons/hicolor/32x32/apps/chromium.png
%{_datadir}/icons/hicolor/32x32/apps/chromium.xpm
%{_datadir}/icons/hicolor/48x48/apps/chromium.png
%{_datadir}/icons/hicolor/64x64/apps/chromium.png
%{_datadir}/icons/hicolor/128x128/apps/chromium.png
%{_datadir}/icons/hicolor/256x256/apps/chromium.png
%{_mandir}/man1/%{name}.1.gz
%dir %{chromiumdir}
%{chromiumdir}/chromium
%if %{with devel_tools}
%{chromiumdir}/chromedriver
%{chromiumdir}/chrome-sandbox
%endif
%{chromiumdir}/icudtl.dat

#{chromiumdir}/nacl_helper
#{chromiumdir}/nacl_helper_bootstrap
#{chromiumdir}/nacl_irt_x86_64.nexe

%{chromiumdir}/natives_blob.bin
%{chromiumdir}/snapshot_blob.bin
%{chromiumdir}/*.pak
%dir %{chromiumdir}/locales
%{chromiumdir}/locales/*.pak
%dir %{chromiumdir}/PepperFlash/

%files libs
%{chromiumdir}/lib*.so*
%exclude %{chromiumdir}/libwidevinecdm.so
%exclude %{chromiumdir}/libwidevinecdmadapter.so
%exclude %{chromiumdir}/libffmpeg.so

%if %{with devel_tools}
%files chromedriver
%doc AUTHORS
%license LICENSE
%{_bindir}/%{name}-chromedriver
%{chromiumdir}/chromedriver
%endif

%files libs-media
%{chromiumdir}/libffmpeg.so*
# {chromiumdir}/libmedia.so*

%if %{with remote_desktop}
%files -n chrome-remote-desktop
%{crd_path}/chrome-remote-desktop
%{crd_path}/chrome-remote-desktop-host
%{crd_path}/is-remoting-session
%{crd_path}/lib
%{crd_path}/remoting_native_messaging_host
%{crd_path}/remote-assistance-host
%{_sysconfdir}/pam.d/chrome-remote-desktop
%{_sysconfdir}/chromium/remoting_native_messaging_host/
%{_sysconfdir}/opt/chrome/
%{crd_path}/remoting_locales/
%{crd_path}/start-host
%{_unitdir}/chrome-remote-desktop.service
/var/lib/chrome-remote-desktop/
%endif

%changelog

* Wed Aug 16 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  60.0.3112.101-2
- Updated to 60.0.3112.101

* Thu Aug 03 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  60.0.3112.90-2
- Updated to 60.0.3112.90-2

* Sat Jul 08 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  59.0.3071.115-2
- Updated to 59.0.3071.115

* Tue Jun 20 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  59.0.3071.109-2
- Updated to 59.0.3071.109

* Wed May 10 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  58.0.3029.110-2
- Updated to 58.0.3029.110

* Fri May 05 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  58.0.3029.96-2
- Updated to 58.0.3029.96

* Sat Apr 08 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  57.0.2987.133-2
- Updated to 57.0.2987.133

* Tue Mar 28 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  57.0.2987.98-2
- Updated to 57.0.2987.110

* Fri Mar 10 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  57.0.2987.98-2
- Updated to 57.0.2987.98-2

* Thu Mar 02 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  56.0.2924.87-4
- Fix issue with compilation on gcc7, Thanks to Ben Noordhuis

* Mon Feb 06 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  56.0.2924.87-2
- Updated to 56.0.2924.87

* Thu Jan 26 2017 - David Vasquez <davidjeremias82 AT gmail DOT com>  56.0.2924.76-2
- Updated to 56.0.2924.76
- Renamed to chromium-freeworld

* Sun Dec 18 2016 - David Vasquez <davidjeremias82 AT gmail DOT com>  55.0.2883.87-2
- Updated to 55.0.2883.87

* Fri Dec 02 2016 - David Vasquez <davidjeremias82 AT gmail DOT com>  55.0.2883.75-2
- Updated to 55.0.2883.75

* Thu Dec 01 2016 - David Vasquez <davidjeremias82 AT gmail DOT com>  54.0.2840.100-3
- Conditional task

* Sat Nov 12 2016 - David Vasquez <davidjeremias82 AT gmail DOT com>  54.0.2840.100-2
- Updated to 54.0.2840.100

* Mon Nov 07 2016 - David Vasquez <davidjeremias82 AT gmail DOT com>  54.0.2840.90-2
- Updated to 54.0.2840.90

* Mon Oct 31 2016 - David Vasquez <davidjeremias82 AT gmail DOT com>  54.0.2840.71-3
- Initial build
