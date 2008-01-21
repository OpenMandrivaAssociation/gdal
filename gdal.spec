#%define __libtoolize /bin/true
%define _requires_exceptions devel(libogdi31(64bit))

%define major 1
%define libname %mklibname %{name} %{major}

# Build gdal against libgrass. It is better to instead compile the new plugin
# which builds against grass itself (and thus has more features than the
# libgrass5 version
%define build_libgrass 0
%{?with_libgrass: %define build_libgrass 1}

Name: gdal
Version: 1.5.0
Release: %mkrel 1
Summary: The Geospatial Data Abstraction Library (GDAL)
Group: Sciences/Geosciences
License: MIT
URL: http://www.gdal.org/
Source: ftp://ftp.remotesensing.org/pub/gdal/%{name}-%{version}.tar.gz
BuildRequires:	libpng-devel
BuildRequires:	zlib-devel
BuildRequires:	geotiff-devel >= 1.2.0
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

%package -n %{libname}-devel
Summary: Development files for using the GDAL library
Group: Sciences/Geosciences
Requires: %{libname} = %{version}-%{release}
Provides: lib%{name}-devel = %{version}
Provides: %{name}-devel = %{version}
%description -n %{libname}-devel
Development files for using the GDAL library

%prep
%setup -q

# fix some exec bits
chmod -x alg/gdal_tps.cpp
chmod -x apps/nearblack.cpp
chmod -x frmts/jpeg/gdalexif.h
chmod -x ogr/ogrsf_frmts/ogdi/ogrogdi.h
chmod -x ogr/ogrsf_frmts/ogdi/ogrogdilayer.cpp
chmod -x ogr/ogrsf_frmts/ogdi/ogrogdidatasource.cpp
chmod -x ogr/ogrsf_frmts/ogdi/ogrogdidriver.cpp


%build
# fix hardcoded issues
sed -i 's|@LIBTOOL@|%{_bindir}/libtool|g' GDALmake.opt.in
sed -i 's|-L\$with_cfitsio -L\$with_cfitsio\/lib -lcfitsio|-lcfitsio|g' configure
sed -i 's|-I\$with_cfitsio|-I\$with_cfitsio\/include\/cfitsio|g' configure
sed -i 's|-L\$with_netcdf -L\$with_netcdf\/lib -lnetcdf|-lnetcdf|g' configure
sed -i 's|-L\$DODS_LIB -ldap++|-ldap++|g' configure
sed -i 's|-L\$with_ogdi -L\$with_ogdi\/lib -logdi|-logdi|g' configure
sed -i 's|-L\$with_jpeg -L\$with_jpeg\/lib -ljpeg|-ljpeg|g' configure
sed -i 's|-L\$with_libtiff\/lib -ltiff|-ltiff|g' configure
sed -i 's|-L\$with_grass\/lib||g' configure
sed -i 's|-lgeotiff -L$with_geotiff $LIBS|-lgeotiff $LIBS|g' configure
sed -i 's|-L\$with_geotiff\/lib -lgeotiff $LIBS|-lgeotiff $LIBS|g' configure
sed -i 's|-lmfhdf -ldf $LIBS|-L$libdir/hdf -lmfhdf -ldf $LIBS|g' configure
sed -i 's|-logdi31|-logdi|g' configure

# append some path for few libs
export CPPFLAGS="`pkg-config ogdi --cflags`"
export CPPFLAGS="$CPPFLAGS -I%{_includedir}/netcdf-3"
export CPPFLAGS="$CPPFLAGS -I%{_includedir}/hdf"
export CPPFLAGS="$CPPFLAGS -I%{_includedir}/libgeotiff"
export CPPFLAGS="$CPPFLAGS `dap-config --cflags`"
export CFLAGS="$RPM_OPT_FLAGS" 
export CXXFLAGS="$RPM_OPT_FLAGS"

%configure2_5x \
	--prefix=%{_prefix} \
        --includedir=%{_includedir}/%{name}/ \
        --datadir=%{_datadir}/%{name}/ \
        --with-threads      \
        --with-dods-root=%{_libdir} \
        --with-ogdi=`ogdi-config --libdir` \
        --with-cfitsio=%{_prefix} \
        --with-geotiff=external   \
        --with-tiff=external      \
        --with-libtiff=external   \
        --with-libz               \
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
        --with-xerces-inc=%{_includedir} \
        --without-pcraster        \
        --enable-shared           \
        %if %{build_libgrass}
    	    --with-libgrass             \
    	    --with-grass=%{_prefix}     \
    	    --disable-static
        %endif
        
# fixup hardcoded wrong compile flags.
cp GDALmake.opt GDALmake.opt.orig
sed -e "s/^CFLAGS.*$/CFLAGS=$CFLAGS/" \
-e "s/^CXXFLAGS.*$/CXXFLAGS=$CXXFLAGS/" \
-e "s/^FFLAGS.*$/FFLAGS=$FFLAGS/" \
-e "s/ cfitsio / /" \
-e "s/-ldap++/-ldap -ldapclient -ldapserver/" \
-e "s/-L\$(INST_LIB) -lgdal/-lgdal/" \
GDALmake.opt.orig > GDALmake.opt
rm GDALmake.opt.orig

# fixup non-existent lookup dir
mkdir -p external/include	

#%make breaks build
make
make docs

%install
rm -Rf %{buildroot}

# fix include header instalation issue
cat GNUmakefile | grep -v "\$(INSTALL_DIR) \$(DESTDIR)\$(INST_INCLUDE)" | \
                  grep -v "\$(INSTALL_DIR) \$(DESTDIR)\$(INST_DATA)" \
		 > GNUmakefile.tmp; mv -f GNUmakefile.tmp GNUmakefile

%makeinstall \
INST_PREFIX=%{buildroot}/%{_prefix} \
INST_INCLUDE=%{buildroot}/%{_includedir} \
INST_DATA=%{buildroot}/%{_datadir}/gdal \
INST_LIB=%{buildroot}/%{_libdir} \
INST_BIN=%{buildroot}/%{_bindir} \
INST_PYMOD=%{buildroot}/%{python_sitearch} \
INST_MAN=%{buildroot}/%{_mandir} 

perl -pi -e 's,%{_prefix}/lib/,%{_libdir}/,g' %{buildroot}/%{_libdir}/libgdal.la

%multiarch_binaries %{buildroot}%{_bindir}/gdal-config
#%multiarch_includes %{buildroot}%{_includedir}/cpl_config.h

# fix some exec bits
find %{buildroot}%{perl_vendorarch} -name "*.so" -exec chmod 755 '{}' \;

# build and include more docs
mkdir -p doc/frmts; find frmts -name "*.html" -exec install -m 644 '{}' doc/frmts/ \;
mkdir -p doc/ogrsf_frmts; find ogr/ogrsf_frmts -name "*.html" -exec install -m 644 '{}' doc/ogrsf_frmts \;

# some commented out are broken for now
pushd doc; doxygen *.dox; popd
pushd ogr/ogrsf_frmts; doxygen *.dox; popd
pushd doxygen; popd

# cleanup junks
rm -rf %{buildroot}%{_includedir}/%{name}/%{name}
for junk in {*.a,*.la,*.bs,.exists,.packlist,.cvsignore} ; do
find %{buildroot} -name "$junk" -exec rm -rf '{}' \;
done

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf "$RPM_BUILD_ROOT"

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_datadir}/gdal/
%{_bindir}/ogr*
%{_bindir}/gdal*
%{_bindir}/nearblack
%exclude %{_bindir}/gdal-config
%{_mandir}/man?/*
%doc NEWS VERSION

%files -n %{libname}-devel
%defattr(-,root,root)
%doc html ogr/html 
%doc ogr/wcts/html 
%doc ogr/ogrsf_frmts/html
%{_bindir}/%{name}-config
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%multiarch %{multiarch_bindir}/gdal-config
%multiarch %{multiarch_includedir}/cpl_config.h
%{_mandir}/man1/%{name}-config*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}
%{_libdir}/*.so.%{major}.*

%ifnarch x86_64
%files python
%defattr(-,root,root,-)
%exclude %{_bindir}/*.py?
%attr(0755,root,root) %{_bindir}/*.py
%{_mandir}/man1/pct2rgb.1.*
%{_mandir}/man1/rgb2pct.1.*
%{_mandir}/man1/gdal_merge.1.*
%py_sitedir/*
%{_bindir}/*.py
%doc pymod/samples
%endif
