%define Werror_cflags %{nil}
%define _disable_lto 1

%if %{_use_internal_dependency_generator}
%define __noautoreq 'devel\\(libogdi31.*|devel\\(libcfitsio.*|libgrass.*'
%else
%define _requires_exceptions devel\(libogdi31.*\)\\|devel\(libcfitsio.*\)\\|libgrass
%endif

%define major 31
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

Summary:	The Geospatial Data Abstraction Library (GDAL)
Name:		gdal
Version:	3.5.1
Release:	1
Group:		Sciences/Geosciences
License:	MIT
URL:		https://gdal.org/
Source0:	https://download.osgeo.org/gdal/%{version}/%{name}-%{version}.tar.xz
Patch2:		gdal-2.3.2-libtoolsucks.patch
Patch3:		gdal-3.1.0-no-Lusrlib.patch
Patch4:		gdal-fix-pythontools-install.patch
# cb - seems to use the /usr/bin/libtool as a linker which breaks
Patch5:		gdal-fix-python.patch

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

%description
The Geospatial Data Abstraction Library (GDAL) is a unifying
C/C++ API for accessing raster geospatial data, and currently
includes formats like GeoTIFF, Erdas Imagine, Arc/Info
Binary, CEOS, DTED, GXF, and SDTS. It is intended to provide
efficient access, suitable for use in viewer applications,
and also attempts to preserve coordinate systems and metadata.
Python, C, and C++ interfaces are available.

%files
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

#---------------------------------------------------------------------------

%prep
%autosetup -p1

aclocal -I m4
autoconf

find . -name '*.h' -o -name '*.cpp' -executable -exec chmod a-x {} \;
find . -name '*.h' -o -name '*.cpp' -executable -exec chmod a+r {} \;

# Replace hard-coded library- and include paths
sed -i 's|@LIBTOOL@|%{_bindir}/libtool|g' GDALmake.opt.in

# Fix mandir
sed -i "s|^mandir=.*|mandir='\${prefix}/share/man'|" configure

%build
cp -f %{_datadir}/gettext/config.rpath .
libtoolize -fiv
aclocal -I m4
autoconf

%configure \
	--datadir=%_datadir/gdal \
	--mandir=%_mandir \
	--includedir=%_includedir/gdal \
	--with-dods-root=no \
	--with-ogdi=%{ogdidir} \
	--with-cfitsio=yes \
	--with-geotiff=internal \
	--with-libtiff \
	--with-libz \
	--with-liblzma=yes \
	--with-netcdf=%_prefix \
	--with-hdf5 \
	--with-geos \
	--with-jasper \
	--with-png \
	--with-gif \
	--with-jpeg \
	--with-odbc \
	--with-sqlite3 \
	--with-mysql \
	--with-curl \
	--with-python \
	--with-xerces \
	--with-xerces-lib='-lxerces-c' \
	--with-xerces-inc=%_includedir \
	--without-pcraster \
	--without-local \
	%if %{build_libgrass}
		--with-grass=%_libdir/grass64 \
	%endif
	--with-threads

sed -i -e 's,^INST_MAN.*,INST_MAN = %{_mandir},g' GDALmake.opt

%make_build
#make docs

%install
mkdir -p %{buildroot}/%py_platsitedir
export PYTHONPATH="%{buildroot}/%py_platsitedir"
export DESTDIR=%{buildroot}
unset PYTHONDONTWRITEBYTECODE
%make_install install-man

find %{buildroot}%{py_platsitedir} -name '*.py' -exec chmod a-x {} \;
