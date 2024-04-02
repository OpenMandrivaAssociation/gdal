%define Werror_cflags %{nil}
%define _disable_lto 1

%if %{_use_internal_dependency_generator}
%define __noautoreq 'devel\\(libogdi31.*|devel\\(libcfitsio.*|libgrass.*'
%else
%define _requires_exceptions devel\(libogdi31.*\)\\|devel\(libcfitsio.*\)\\|libgrass
%endif
%global __requires_exclude cmake\\(OpenJPEG\\)

%define major 34
%define oldlibname %mklibname %{name} 30
%define libname %mklibname %{name}
%define devname %mklibname %{name} -d

# Build gdal against libgrass. It is better to instead compile the new plugin
# which builds against grass itself (and thus has more features than the
# libgrass5 version)
# In fact, building with direct grass support will break gdal on every grass
# upgrade, see http://n2.nabble.com/qgis-%2B-grass-plugin-%3D-gdal-problem-tp2394932p2405146.html
%define build_libgrass 0
%{?with_libgrass: %define build_libgrass 1}

%define ogdidir %{_includedir}
%define ogdidir %{_includedir}/ogdi

%bcond_with mono
%bcond_without java

Summary:	The Geospatial Data Abstraction Library (GDAL)
Name:		gdal
Version:	3.8.4
Release:	3
Group:		Sciences/Geosciences
License:	MIT
URL:		https://gdal.org/
Source0:	https://download.osgeo.org/gdal/%{version}/%{name}-%{version}.tar.xz
Patch0:		gdal-3.6.3-c++17.patch
Patch1:		gdal-3.6.3-openjdk-18.patch
Patch2:		gdal-fix-missing-includes.patch
Patch3:		gdal-3.7.2-work-around-duplicate-curl-cmake-checks.patch
#Patch4:		gdal-fix-pythontools-install.patch
# cb - seems to use the /usr/bin/libtool as a linker which breaks
#Patch5:		gdal-fix-python.patch

BuildRequires:	libtool-devel
BuildRequires:	zlib-devel
BuildRequires:	geotiff-devel >= 1.2.0
BuildRequires:	png-devel
BuildRequires:	giflib-devel
BuildRequires:	postgresql-devel >= 9.0
BuildRequires:	jpeg-devel
BuildRequires:	lzma-devel
BuildRequires:	pkgconfig(proj) >= 4.4.7
BuildRequires:	pkgconfig(python3)
BuildRequires:	doxygen
BuildRequires:	pkgconfig(libtirpc)
BuildRequires:	pkgconfig(libdeflate)
BuildRequires:	locales-extra-charsets
BuildRequires:	qhull-devel
# Can be used, but lives in unsupported
#BuildRequires:	pkgconfig(freexl)
%if %{build_libgrass}
Requires:	grass >= 6.4.0
BuildRequires:	grass
%else
BuildConflicts:	%mklibname -d grass 5 0
%endif
BuildRequires:	jasper-devel
BuildRequires:	geos-devel >= 2.2.3
BuildRequires:	netcdf-devel >= 3.6.2
BuildRequires:	ogdi-devel
BuildRequires:	pkgconfig(cfitsio)
BuildRequires:	pkgconfig(poppler)
BuildRequires:	pkgconfig(OpenEXR)
BuildRequires:	pkgconfig(libarchive)
#Causes build crash with llvm18
#BuildRequires:	pkgconfig(libopenjp2)
BuildRequires:	pkgconfig(liblz4)
BuildRequires:	pkgconfig(OpenCL)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(cryptopp)
BuildRequires:	pkgconfig(geotiff)
BuildRequires:	pkgconfig(libpodofo)
BuildRequires:	pkgconfig(libpcre2-posix)
BuildRequires:	pkgconfig(libpcre2-8)
BuildRequires:	pkgconfig(libpcre2-16)
BuildRequires:	pkgconfig(libpcre2-32)
BuildRequires:	pkgconfig(libwebp)
BuildRequires:	pkgconfig(json-c)
BuildRequires:	python-numpy-devel
BuildRequires:	python-setuptools
BuildRequires:	sqlite3-devel
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(libunwind-llvm)
BuildRequires:	mysql-devel
#BuildRequires:	libdap-devel
#BuildRequires:	librx-devel
BuildRequires:	unixODBC-devel
BuildRequires:	xerces-c-devel
BuildRequires:	hdf5-devel
BuildRequires:	swig
BuildRequires:	bison
%if %{with java}
BuildRequires:	jdk-current
BuildRequires:	jre-gui-current
BuildRequires:	ant
%endif
%if %{with mono}
BuildRequires:	mono
%endif
BuildRequires:	cmake ninja

%description
The Geospatial Data Abstraction Library (GDAL) is a unifying
C/C++ API for accessing raster geospatial data, and currently
includes formats like GeoTIFF, Erdas Imagine, Arc/Info
Binary, CEOS, DTED, GXF, and SDTS. It is intended to provide
efficient access, suitable for use in viewer applications,
and also attempts to preserve coordinate systems and metadata.
Python, C, and C++ interfaces are available.

%files
%{_datadir}/bash-completion/completions/*
%{_datadir}/gdal/
%{_bindir}/*
%{_mandir}/man1/*

%exclude %{_bindir}/gdal-config
%doc VERSION

#---------------------------------------------------------------------------

%package -n python-%{name}
Summary: The Python bindings for the GDAL library
Group: Sciences/Geosciences
Requires: %{libname} = %{version}
%rename gdal-python

%description -n python-%{name}
The Python bindings for the GDAL library

%files -n python-%{name}
%py_platsitedir/*

#---------------------------------------------------------------------------

%package -n %{libname}
Summary: Libraries required for the GDAL library
Group: System/Libraries
Provides: lib%{name} = %{version}
Obsoletes: %{oldlibname} < %{EVRD}

%description -n %{libname}
Libraries required for the GDAL library

%files -n %{libname}
%{_libdir}/*.so.%{major}*
%{_libdir}/gdalplugins

#---------------------------------------------------------------------------
%if %{with mono}
%package csharp
Summary: C# bindings for the GDAL library
Group: Development/Java

%description csharp
C# bindings for the GDAL library

%files csharp
%{_datadir}/csharp/*
%endif

#---------------------------------------------------------------------------
%if %{with java}
%package java
Summary: Java bindings for the GDAL library
Group: Development/Java

%description java
Java bindings for the GDAL library

%files java
%{_datadir}/java/gdal*
%{_libdir}/jni/libgdalalljni.so
%endif

#---------------------------------------------------------------------------

%package -n %{devname}
Summary: Development files for using the GDAL library
Group: Development/C
Requires: %{libname} = %{version}-%{release}
Provides: lib%{name}-devel = %{version}
Provides: %{name}-devel = %{version}

%description -n %{devname}
Development files for using the GDAL library

%files -n %{devname}
%{_bindir}/%{name}-config
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/pkgconfig/gdal.pc
%{_libdir}/cmake/gdal

#---------------------------------------------------------------------------

%prep
%autosetup -p1
find . -name '*.h' -o -name '*.cpp' -executable -exec chmod a-x {} \;
find . -name '*.h' -o -name '*.cpp' -executable -exec chmod a+r {} \;

# DOS madness in files copied from ancient zlib...
sed -i -e 's,FAR ,,g' frmts/zlib/contrib/infback9/*.{c,h} port/cpl_vsil_gzip.cpp
sed -i -e 's,zmemcpy,memcpy,g' frmts/zlib/contrib/infback9/infback9.c

%if %{with java}
. %{_sysconfdir}/profile.d/90java.sh
%endif

# PoDoFo forced off because gdal isn't compatible with releases >= 0.10
%cmake \
	-DGDAL_USE_PNG_INTERNAL:BOOL=OFF \
	-DGDAL_USE_ZLIB_INTERNAL:BOOL=OFF \
	-DGDAL_USE_GIF_INTERNAL:BOOL=OFF \
	-DGDAL_USE_TIFF_INTERNAL:BOOL=OFF \
	-DGDAL_USE_GEOTIFF_INTERNAL:BOOL=OFF \
	-DGDAL_USE_JPEG_INTERNAL:BOOL=OFF \
	-DGDAL_USE_PODOFO:BOOL=ON \
	-G Ninja

%build
%if %{with java}
. %{_sysconfdir}/profile.d/90java.sh
%endif
%ninja_build -C build

%install
%if %{with java}
. %{_sysconfdir}/profile.d/90java.sh
%endif
#mkdir -p %{buildroot}/%py_platsitedir
#export PYTHONPATH="%{buildroot}/%py_platsitedir"
#export DESTDIR=%{buildroot}
%ninja_install -C build

find %{buildroot}%{py_platsitedir} -name '*.py' -exec chmod a-x {} \;
