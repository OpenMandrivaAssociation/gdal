#%define __libtoolize /bin/true
%define _requires_exceptions devel(libogdi31(64bit))

%define major 1
%define libname %mklibname %{name} %{major}

%define build_geotiff 1
%{?_without_geotiff: %define build_geotiff 0}

# Build gdal against libgrass. It is better to instead compile the new plugin
# which builds against grass itself (and thus has more features than the
# libgrass5 version
%define build_libgrass 0
%{?with_libgrass: %define build_libgrass 1}

Name: gdal
Version: 1.4.0
Release: %mkrel 1
Summary: The Geospatial Data Abstraction Library (GDAL)
Group: Sciences/Geosciences
License:	MIT
URL: http://www.remotesensing.org/gdal/
Source: ftp://ftp.remotesensing.org/pub/gdal/%{name}-%{version}.tar.bz2
BuildRequires:	libpng-devel
BuildRequires:	zlib-devel
%if %build_geotiff
BuildRequires:	libgeotiff-devel >= 1.2.0
%endif
BuildRequires:	libpng-devel
BuildRequires:	libungif-devel
BuildRequires:	postgresql-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libproj-devel >= 4.4.7
%if %{build_libgrass}
BuildRequires:	libgrass5-devel
%else
BuildConflicts:	%mklibname -d grass 5 0
%endif
BuildRequires:	libjasper-devel
BuildRequires: libgeos-devel >= 2.2.3
#HDF broken
Buildconflicts: HDF
BuildRequires:	netcdf-devel
BuildRequires:	ogdi-devel
BuildRequires:	cfitsio-devel
BuildRequires:	python-numeric-devel
BuildRequires:	sqlite3-devel
BuildRequires:	mysql-devel
%py_requires -d 
Requires:	%{libname} = %{version}
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
Group: 		Sciences/Geosciences
#Requires:
Requires: %{libname} = %{version}
%description python
The Python bindings for the GDAL library

%package -n %{libname}
Summary: Libraries required for the GDAL library
Group: 		Sciences/Geosciences
Provides: lib%{name} = %{version}
%description -n %{libname}
Libraries required for the GDAL library

%package -n %{libname}-devel
Summary: Development files for using the GDAL library
Group: 		Sciences/Geosciences
Requires: %{libname} = %{version}-%{release}
Provides: lib%{name}-devel = %{version}
Provides: %{name}-devel = %{version}
%description -n %{libname}-devel
Development files for using the GDAL library

%prep
%setup -q

%build
%configure2_5x \
	--with-libz \
	--with-png \
%if %build_geotiff	
	--with-libtiff \
	--with-geotiff \
%else
	--with-libtiff=internal \
	--with-geotiff=internal \
%endif	
	--with-gif \
	--with-jpeg \
	--with-ogr \
%if %{build_libgrass}
	--with-grass \
%endif
	--with-sqlite \
	--with-pg \
	--with-mysql
perl -pi -e 's/^(CX*_OPTFLAGS.*$)/$1 -fPIC/g' GDALmake.opt
%make

%install
rm -Rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT/%{_prefix}
mkdir -p $RPM_BUILD_ROOT/%{_libdir}/python%{pyver}/site-packages
%makeinstall \
INST_PREFIX=%{buildroot}/%{_prefix} \
INST_INCLUDE=%{buildroot}/%{_includedir} \
INST_DATA=%{buildroot}/%{_datadir}/gdal \
INST_LIB=%{buildroot}/%{_libdir} \
INST_BIN=%{buildroot}/%{_bindir} \
INST_PYMOD=%{buildroot}/%{_libdir}/python%{pyver}/site-packages \
INST_MAN=%{buildroot}/%{_mandir} 

perl -pi -e 's,%{_prefix}/lib/,%{_libdir}/,g' %{buildroot}/%{_libdir}/libgdal.la

%if %mdkversion >= 1020
%multiarch_binaries %{buildroot}%{_bindir}/gdal-config
%multiarch_includes %{buildroot}%{_includedir}/cpl_config.h
%endif

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf "$RPM_BUILD_ROOT"

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_datadir}/gdal/
%{_bindir}/ogr*
%{_bindir}/gdal*
%exclude %{_bindir}/gdal-config
%{_mandir}/man?/*
%doc NEWS VERSION

%files -n %{libname}-devel
%defattr(-,root,root)
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_includedir}/*.h
%if %mdkversion >= 1020
%multiarch %{multiarch_bindir}/gdal-config
%multiarch %{multiarch_includedir}/cpl_config.h
%endif
%{_bindir}/gdal-config
# doc html/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%ifnarch x86_64
%files python
%defattr(-,root,root)
%py_sitedir/*
%{_bindir}/*.py
%doc pymod/samples
%endif



