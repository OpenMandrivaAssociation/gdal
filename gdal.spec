%global	Werror_cflags %{nil}
%global	_disable_lto 1
%global	_disable_ld_no_undefined	1

%if %{_use_internal_dependency_generator}
%global	__noautoreq 'devel\\(libogdi31.*|devel\\(libcfitsio.*|libgrass.*'
%else
%global	_requires_exceptions devel\(libogdi31.*\)\\|devel\(libcfitsio.*\)\\|libgrass
%endif
%global __requires_exclude cmake\\(OpenJPEG\\)

%define	major 38
%define	oldlibname %mklibname %{name} 30
%define	libname %mklibname %{name}
%define	devname %mklibname %{name} -d

# Build gdal against libgrass. It is better to instead compile the new plugin
# which builds against grass itself (and thus has more features than the
# libgrass5 version)
# In fact, building with direct grass support will break gdal on every grass
# upgrade, see http://n2.nabble.com/qgis-%%2B-grass-plugin-%%3D-gdal-problem-tp2394932p2405146.html
%define	build_libgrass 0
%{?with_libgrass: %define build_libgrass 1}

%define	ogdidir %{_includedir}
%define	ogdidir %{_includedir}/ogdi

%bcond_with mono
%bcond_without java

Summary:	The Geospatial Data Abstraction Library (GDAL)
Name:	gdal
Version:	3.12.0
Release:	1
Group:	Sciences/Geosciences
License:	MIT
Url:		https://gdal.org/
Source0:	https://download.osgeo.org/gdal/%{version}/%{name}-%{version}.tar.xz
Source100:	gdal.rpmlintrc
Patch0:		gdal-fix-missing-includes.patch
Patch1:		gdal-3.7.2-work-around-duplicate-curl-cmake-checks.patch
Patch2:		gdal-3.10.0-poppler-25.patch
%if %{with java}
BuildRequires:	ant
BuildRequires:	jdk-current
BuildRequires:	jre-gui-current
%endif
BuildRequires:	bison
# For clang-scan-deps
BuildRequires:	clang-tools
BuildRequires:	doxygen
%if %{build_libgrass}
BuildRequires:	grass
Requires:	grass >= 6.4.0
%else
BuildConflicts:	%mklibname -d grass 5 0
%endif
BuildRequires:	locales-extra-charsets
BuildRequires:	python-setuptools
BuildRequires:	swig
BuildRequires:	gettext-devel
BuildRequires:	giflib-devel
BuildRequires:	hdf5-devel
BuildRequires:	make
# Missing, but needed?
#BuildRequires:	libdap-devel
#BuildRequires:	librx-devel
BuildRequires:	libtool-devel
# Cmake searches for this
BuildRequires:	%{_lib}zstd-static-devel
BuildRequires:	mysql-devel
BuildRequires:	postgresql-devel >= 9.0
BuildRequires:	python-numpy-devel
BuildRequires:	pkgconfig(cfitsio)
BuildRequires:	pkgconfig(cryptopp)
BuildRequires:	pkgconfig(expat)
# Can be used, but lives in Extra
#BuildRequires:	pkgconfig(freexl)
BuildRequires:	pkgconfig(geos) >= 2.2.3
BuildRequires:	pkgconfig(geotiff)
BuildRequires:	pkgconfig(jasper)
BuildRequires:	pkgconfig(json-c)
BuildRequires:	pkgconfig(libarchive)
BuildRequires:	pkgconfig(libcurl) >= 7.68
BuildRequires:	pkgconfig(libdeflate)
BuildRequires:	pkgconfig(libgeotiff) >= 1.2.0
BuildRequires:	pkgconfig(libopenjp2)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(liblz4)
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(libpodofo)
BuildRequires:	pkgconfig(libpcre2-8)
BuildRequires:	pkgconfig(libpcre2-16)
BuildRequires:	pkgconfig(libpcre2-32)
BuildRequires:	pkgconfig(libpcre2-posix)
# Can be used, but lives in Extra
#BuildRequires:	pkgconfig(spatialite)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(libtirpc)
BuildRequires:	pkgconfig(libunwind-llvm)
BuildRequires:	pkgconfig(libwebp)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(libzstd)
BuildRequires:	pkgconfig(muparser)
BuildRequires:	pkgconfig(netcdf) >= 3.6.2
BuildRequires:	pkgconfig(odbc)
BuildRequires:	pkgconfig(ogdi)
BuildRequires:	pkgconfig(OpenCL)
BuildRequires:	pkgconfig(OpenEXR)
BuildRequires:	pkgconfig(poppler)
BuildRequires:	pkgconfig(proj) >= 4.4.7
BuildRequires:	pkgconfig(python3)
BuildRequires:	pkgconfig(qhullcpp)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(xerces-c)
BuildRequires:	pkgconfig(zlib)

%if %{with mono}
BuildRequires:	mono
%endif

BuildSystem:	cmake
BuildOption:	-DGDAL_USE_PNG_INTERNAL:BOOL=OFF
BuildOption:	-DGDAL_USE_ZLIB_INTERNAL:BOOL=OFF
BuildOption:	-DGDAL_USE_GIF_INTERNAL:BOOL=OFF
BuildOption:	-DGDAL_USE_TIFF_INTERNAL:BOOL=OFF
BuildOption:	-DGDAL_USE_GEOTIFF_INTERNAL:BOOL=OFF
BuildOption:	-DGDAL_USE_JPEG_INTERNAL:BOOL=OFF
BuildOption:	-DGDAL_USE_PODOFO:BOOL=ON
BuildOption:	-DBUILD_TESTING:BOOL=OFF

%description
The Geospatial Data Abstraction Library (GDAL) is a unifying C/C++ API for
accessing raster geospatial data, and currently includes formats like GeoTIFF,
Erdas Imagine, Arc/Info Binary, CEOS, DTED, GXF, and SDTS. It is intended
to provide efficient access, suitable for use in viewer applications, and also
attempts to preserve coordinate systems and metadata.
Python, C, and C++ interfaces are available.

%files
%doc VERSION
%exclude %{_bindir}/%{name}-config
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/%{name}/
%{_datadir}/bash-completion/completions/*

#---------------------------------------------------------------------------

%package -n python-%{name}
Summary: The Python bindings for the GDAL library
Group: Sciences/Geosciences
Requires: %{libname} = %{version}
%rename %{name}-python

%description -n python-%{name}
The Python bindings for the GDAL library.

%files -n python-%{name}
%{py_platsitedir}/GDAL-%{version}-py%{pyver}.egg-info/*
%{py_platsitedir}/osgeo/*
%{py_platsitedir}/osgeo_utils/*

#---------------------------------------------------------------------------

%package -n %{libname}
Summary: Libraries required for the GDAL library
Group: System/Libraries
Provides: lib%{name} = %{version}
Obsoletes: %{oldlibname} < %{EVRD}

%description -n %{libname}
Libraries required for the GDAL library.

%files -n %{libname}
%{_libdir}/libgdal.so.%{major}*
%{_libdir}/gdalplugins

#---------------------------------------------------------------------------

%if %{with mono}
%package csharp
Summary: C# bindings for the GDAL library
Group: Development/Java

%description csharp
C# bindings for the GDAL library.

%files csharp
%{_datadir}/csharp/*
%endif

#---------------------------------------------------------------------------

%if %{with java}
%package java
Summary: Java bindings for the GDAL library
Group: Development/Java

%description java
Java bindings for the GDAL library.

%files java
%{_datadir}/java/%{name}*.jar
%{_datadir}/java/%{name}-%{version}.pom
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
%{_libdir}/libgdal.so
%{_includedir}/*
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/cmake/%{name}/*

#---------------------------------------------------------------------------

%prep
%autosetup -p1

find . -name '*.h' -o -name '*.cpp' -executable -exec chmod a-x {} \;
find . -name '*.h' -o -name '*.cpp' -executable -exec chmod a+r {} \;

# DOS madness in files copied from ancient zlib...
sed -i -e 's,FAR ,,g' frmts/zlib/contrib/infback9/*.{c,h} port/cpl_vsil_gzip.cpp
sed -i -e 's,zmemcpy,memcpy,g' frmts/zlib/contrib/infback9/infback9.c

%conf -p
%if %{with java}
%{_sysconfdir}/profile.d/90java.sh
%endif

%build -p
%if %{with java}
%{_sysconfdir}/profile.d/90java.sh
%endif

%install -p
%if %{with java}
%{_sysconfdir}/profile.d/90java.sh
%endif

%install -a
# Fix files with wrong python shebangs
sed -i 's|^#!python|#!/usr/bin/python|' %{buildroot}%{_bindir}/*.py

# Fix perms for python files
find %{buildroot}%{py_platsitedir} -name '*.py' -exec chmod a-x {} \;
find %{buildroot}%{py_platsitedir}/osgeo_utils -name '*.py' -exec chmod +x {} \;
chmod -x %{buildroot}%{py_platsitedir}/osgeo_utils/__init__.py
chmod -x %{buildroot}%{py_platsitedir}/osgeo_utils/auxiliary/__init__.py
chmod -x %{buildroot}%{py_platsitedir}/osgeo_utils/auxiliary/osr_util.py
chmod -x %{buildroot}%{py_platsitedir}/osgeo_utils/samples/__init__.py
chmod -x %{buildroot}%{py_platsitedir}/osgeo_utils/samples/gdal_minmax_location.py
chmod -x %{buildroot}%{py_platsitedir}/osgeo_utils/samples/gdallocationinfo.py
