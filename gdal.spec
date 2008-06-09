%define _requires_exceptions devel\(libogdi31.*\)\\|devel\(libcfitsio.*\)

%define major 1
%define libname %mklibname %{name} %{major}
%define libnamedev %mklibname %{name} -d
%define libnamedevstat %mklibname %{name} -d -s

# Build gdal against libgrass. It is better to instead compile the new plugin
# which builds against grass itself (and thus has more features than the
# libgrass5 version
%define build_libgrass 0
%{?with_libgrass: %define build_libgrass 1}

Name: gdal
Version: 1.5.1
Release: %mkrel 1
Summary: The Geospatial Data Abstraction Library (GDAL)
Group: Sciences/Geosciences
License: MIT
URL: http://www.gdal.org/
Source: ftp://ftp.remotesensing.org/pub/gdal/%{name}-%{version}.tar.gz
Patch0:    %{name}-gcc43.patch
Patch1:    %{name}-perl510.patch
BuildRequires:	libpng-devel
BuildRequires:	zlib-devel
BuildRequires:	geotiff-devel >= 1.2.0
BuildRequires:	libpng-devel
BuildRequires:	libungif-devel
BuildRequires:	postgresql-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libproj-devel >= 4.4.7
BuildRequires:  doxygen
%if %{build_libgrass}
BuildRequires:	libgrass5-devel
%else
BuildConflicts:	%mklibname -d grass 5 0
%endif
BuildRequires:	libjasper-devel
BuildRequires:	libgeos-devel >= 2.2.3
BuildRequires:	hdf5-devel
BuildRequires:	netcdf-devel >= 3.6.2
BuildRequires:	ogdi-devel
BuildRequires:	cfitsio-devel
BuildRequires:	python-numpy-devel
BuildRequires:	sqlite3-devel
BuildRequires:	mysql-devel
BuildRequires:	libdap-devel
BuildRequires:	librx-devel
BuildRequires:	unixODBC-devel
BuildRequires:	xerces-c-devel
BuildRequires:	swig
%py_requires -d 
BuildRoot: 	%{_tmppath}/%{name}-%{version}-root

%description
The Geospatial Data Abstraction Library (GDAL) is a unifying
C/C++ API for accessing raster geospatial data, and currently
includes formats like GeoTIFF, Erdas Imagine, Arc/Info
Binary, CEOS, DTED, GXF, and SDTS. It is intended to provide
efficient access, suitable for use in viewer applications,
and also attempts to preserve coordinate systems and metadata.
Python, C, and C++ interfaces are available.

%package python
Summary: The Python bindings for the GDAL library
Group: Sciences/Geosciences
Requires: %{libname} = %{version}
%description python
The Python bindings for the GDAL library

%package -n %{libname}
Summary: Libraries required for the GDAL library
Group: Sciences/Geosciences
Provides: lib%{name} = %{version}
%description -n %{libname}
Libraries required for the GDAL library

%package -n %{libnamedev}
Summary: Development files for using the GDAL library
Group: Sciences/Geosciences
Requires: %{libname} = %{version}-%{release}
Provides: lib%{name}-devel = %{version}
Provides: %{name}-devel = %{version}

%description -n %{libnamedev}
Development files for using the GDAL library

%package -n %{libnamedevstat}
Summary: Development files for using the GDAL library
Group: Sciences/Geosciences
Requires: %{libnamedev} = %{version}-%{release}

%description -n %{libnamedevstat}
Development files for using the GDAL library



%prep
%setup -q
%patch0 -p0 -b .gcc43
%patch1 -p0 -b .perl510

%build
export CPPFLAGS="${CPPFLAGS} -I%{_includedir}/hdf $(dap-config --cflags) -I%{_includedir}/netcdf-3 -I%{_includedir}/libgeotiff"

sed -i 's|@LIBTOOL@|%{_bindir}/libtool|g' GDALmake.opt.in

%configure2_5x \
	--datadir=%_datadir/gdal \
	--includedir=%_includedir/gdal \
        --with-dods-root=%_prefix \
        --with-ogdi=%_prefix \
        --with-cfitsio=%_prefix \
        --with-geotiff=yes   \
        --with-libtiff=yes   \
        --with-libz=%_prefix      \
        --with-netcdf             \
        --with-hdf5               \
        --with-geos               \
        --with-jasper             \
        --with-png                \
        --with-gif                \
        --with-jpeg               \
        --with-odbc               \
        --with-sqlite             \
        --with-mysql              \
        --with-curl               \
        --with-python             \
        --with-xerces             \
        --with-xerces-lib='-lxerces-c' \
        --with-xerces-inc=%_includedir \
        --without-pcraster        \
        %if %{build_libgrass}
    	    --with-libgrass             \
    	    --with-grass=%_prefix     \
        %endif
        --with-threads
        
make
make docs

%install
rm -Rf %buildroot

%makeinstall_std 
%multiarch_binaries %{buildroot}%{_bindir}/gdal-config


%clean
rm -rf %buildroot

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files
%defattr(-,root,root)
%{_datadir}/gdal/
%{_bindir}/ogr*
%{_bindir}/gdal*
%{_bindir}/nearblack
%exclude %{_bindir}/gdal-config
%doc NEWS VERSION

%files -n %{libnamedev}
%defattr(-,root,root)
%{_bindir}/%{name}-config
%{_libdir}/*.so
%{_includedir}/*
%_docdir/*
%multiarch %{multiarch_bindir}/gdal-config

%files -n %{libnamedevstat}
%defattr(-,root,root)
%{_libdir}/*.a

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_libdir}/*.la

%files python
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/*.py
%py_platsitedir/*
