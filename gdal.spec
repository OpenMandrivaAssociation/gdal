%define _requires_exceptions devel\(libogdi31.*\)\\|devel\(libcfitsio.*\)\\|libgrass

%define major 1
%define libname %mklibname %{name} %{major}
%define libnamedev %mklibname %{name} -d
%define libnamedevstat %mklibname %{name} -d -s

# Build gdal against libgrass. It is better to instead compile the new plugin
# which builds against grass itself (and thus has more features than the
# libgrass5 version)
# In fact, building with direct grass support will break gdal on every grass
# upgrade, see http://n2.nabble.com/qgis-%2B-grass-plugin-%3D-gdal-problem-tp2394932p2405146.html
%define build_libgrass 0
%{?with_libgrass: %define build_libgrass 1}

%define ogdidir %{_includedir}
%if %mdkversion > 201000
%define ogdidir %{_includedir}/ogdi
%endif

Name: gdal
Version: 1.8.0
Release: %mkrel 1
Summary: The Geospatial Data Abstraction Library (GDAL)
Group: Sciences/Geosciences
License: MIT
URL: http://www.gdal.org/
Source: ftp://ftp.remotesensing.org/pub/gdal/%{name}-%{version}.tar.gz
Patch3: gdal-1.6.0-fix-libname.patch
Patch4: gdal-fix-pythontools-install.patch
BuildRequires:	libpng-devel
BuildRequires:	zlib-devel
BuildRequires:	geotiff-devel >= 1.2.0
BuildRequires:	libpng-devel
BuildRequires:	libungif-devel
BuildRequires:	postgresql-devel
BuildRequires:	libjpeg-devel
BuildRequires:	liblzma-devel
BuildRequires:	proj-devel >= 4.4.7
BuildRequires:  doxygen
%if %{build_libgrass}
Requires:	grass >= 6.4.0
BuildRequires:	grass
%else
BuildConflicts:	%mklibname -d grass 5 0
%endif
BuildRequires:	libjasper-devel
BuildRequires:	libgeos-devel >= 2.2.3
BuildRequires:	netcdf-devel >= 3.6.2
BuildRequires:	ogdi-devel
BuildRequires:	cfitsio-devel
BuildRequires:	python-numpy-devel
BuildRequires:	python-setuptools
BuildRequires:	sqlite3-devel
#BuildRequires:	mysql-devel
#BuildRequires:	libdap-devel
BuildRequires:	librx-devel
BuildRequires:	unixODBC-devel
BuildRequires:	xerces-c-devel
BuildRequires:	hdf5-devel
BuildRequires:	swig
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
%py_requires -d

%description python
The Python bindings for the GDAL library

%package -n %{libname}
Summary: Libraries required for the GDAL library
Group: System/Libraries
Provides: lib%{name} = %{version}

%description -n %{libname}
Libraries required for the GDAL library

%package -n %{libnamedev}
Summary: Development files for using the GDAL library
Group: Development/C
Requires: %{libname} = %{version}-%{release}
Provides: lib%{name}-devel = %{version}
Provides: %{name}-devel = %{version}

%description -n %{libnamedev}
Development files for using the GDAL library

%package -n %{libnamedevstat}
Summary: Development files for using the GDAL library
Group: Development/C
Requires: %{libnamedev} = %{version}-%{release}

%description -n %{libnamedevstat}
Development files for using the GDAL library

%prep
%setup -q
%patch3 -p0 -b .libname
%patch4 -p1 -b .pythontools

%build


%configure2_5x \
	--datadir=%_datadir/gdal \
	--includedir=%_includedir/gdal \
        --with-dods-root=no \
        --with-ogdi=%{ogdidir} \
        --with-cfitsio=yes \
        --with-geotiff=internal   \
        --with-libtiff=internal   \
        --with-libz=%_prefix      \
	--with-liblzma=yes        \
        --with-netcdf=%_prefix    \
        --with-hdf5=%_prefix      \
        --with-geos               \
        --with-jasper             \
        --with-png                \
        --with-gif                \
        --with-jpeg               \
        --with-odbc               \
        --with-sqlite3            \
        --with-mysql              \
        --with-curl               \
        --with-python             \
        --with-xerces             \
        --with-xerces-lib='-lxerces-c' \
        --with-xerces-inc=%_includedir \
        --without-pcraster        \
        %if %{build_libgrass}
    	    --with-grass=%_libdir/grass64     \
        %endif
        --with-threads
        
perl -pi -e 's,PYTHON = no,PYTHON = /usr/bin/python,g' GDALmake.opt
make
make docs

%install
rm -Rf %buildroot
mkdir -p %{buildroot}/%py_platsitedir
export PYTHONPATH="%{buildroot}/%py_platsitedir"
export DESTDIR=%{buildroot}
unset PYTHONDONTWRITEBYTECODE
export INST_MAN=%{_mandir}
%makeinstall_std install-man
perl -pi -e 's,%{_prefix}/lib/,%{_libdir}/,g' %{buildroot}/%{_libdir}/libgdal.la

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
%{_bindir}/*
%exclude %{_bindir}/gdal-config
%doc NEWS VERSION

%files -n %{libnamedev}
%defattr(-,root,root)
%{_bindir}/%{name}-config
%{_libdir}/*.so
%{_includedir}/*
%_docdir/*
%{multiarch_bindir}/gdal-config

%files -n %{libnamedevstat}
%defattr(-,root,root)
%{_libdir}/*.a
%{_libdir}/*.la

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*

%files python
%defattr(-,root,root,-)
%py_platsitedir/*
