#
# Conditional build:
%bcond_without	openmp	# OpenMP support
#
Summary:	LAL Simulation library
Summary(pl.UTF-8):	Biblioteka LAL Simulation
Name:		lal-simulation
Version:	4.0.2
Release:	1
License:	GPL v2+
Group:		Libraries
Source0:	http://software.igwn.org/lscsoft/source/lalsuite/lalsimulation-%{version}.tar.xz
# Source0-md5:	0ec4c5f3c1392ad687a26a7a2f91d6b5
Patch0:		%{name}-env.patch
Patch1:		no-Werror.patch
Patch2:		%{name}-lal-swig.patch
URL:		https://wiki.ligo.org/Computing/DASWG/LALSuite
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
BuildRequires:	gsl-devel >= 1.13
BuildRequires:	lal-devel >= 7.2.2
%{?with_openmp:BuildRequires:	libgomp-devel}
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	octave-devel >= 1:3.2.0
BuildRequires:	pkgconfig
BuildRequires:	python3-devel >= 1:3.5
BuildRequires:	python3-numpy-devel >= 1:1.7
BuildRequires:	swig >= 4.1.0
BuildRequires:	swig-python >= 3.0.11
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires:	gsl >= 1.13
Requires:	lal >= 7.2.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LAL wrapping of the Simulation LIGO_LW XML library.

%description -l pl.UTF-8
Obudowanie LAL do biblioteki Simulation LILO_LW XML.

%package devel
Summary:	Header files for lal-simulation library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki lal-simulation
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	lal-devel >= 7.2.2

%description devel
Header files for lal-simulation library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki lal-simulation.

%package static
Summary:	Static lal-simulation library
Summary(pl.UTF-8):	Statyczna biblioteka lal-simulation
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static lal-simulation library.

%description static -l pl.UTF-8
Statyczna biblioteka lal-simulation.

%package -n octave-lalsimulation
Summary:	Octave interface for LAL Simulation
Summary(pl.UTF-8):	Interfejs Octave do biblioteki LAL Simulation
Group:		Applications/Math
Requires:	%{name} = %{version}-%{release}
Requires:	octave-lal >= 7.2.2

%description -n octave-lalsimulation
Octave interface for LAL Simulation.

%description -n octave-lalsimulation -l pl.UTF-8
Interfejs Octave do biblioteki LAL Simulation.

%package -n python3-lalsimulation
Summary:	Python bindings for LAL Simulation
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki LAL Simulation
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python3-lal >= 7.2.2
Requires:	python3-modules >= 1:3.5

%description -n python3-lalsimulation
Python bindings for LAL Simulation.

%description -n python3-lalsimulation -l pl.UTF-8
Wiązania Pythona do biblioteki LAL Simulation.

%prep
%setup -q -n lalsimulation-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal} -I gnuscripts
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_openmp:--disable-openmp} \
	--disable-silent-rules \
	--enable-swig

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/liblalsimulation.la

install -d $RPM_BUILD_ROOT/etc/shrc.d
%{__mv} $RPM_BUILD_ROOT%{_sysconfdir}/*sh $RPM_BUILD_ROOT/etc/shrc.d

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README.md
%attr(755,root,root) %{_bindir}/lalsim-*
%attr(755,root,root) %{_bindir}/lalsimulation_version
%attr(755,root,root) %{_libdir}/liblalsimulation.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblalsimulation.so.31
%{_datadir}/lalsimulation
/etc/shrc.d/lalsimulation-user-env.csh
/etc/shrc.d/lalsimulation-user-env.fish
/etc/shrc.d/lalsimulation-user-env.sh
%{_mandir}/man1/lalsim*.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblalsimulation.so
%{_includedir}/lal/LALSim*.h
%{_includedir}/lal/SWIGLALSimulation*.h
%{_includedir}/lal/SWIGLALSimulation*.i
%{_includedir}/lal/swiglalsimulation.i
%{_pkgconfigdir}/lalsimulation.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/liblalsimulation.a

%files -n octave-lalsimulation
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/octave/*/site/oct/*/lalsimulation.oct

%files -n python3-lalsimulation
%defattr(644,root,root,755)
%dir %{py3_sitedir}/lalsimulation
%attr(755,root,root) %{py3_sitedir}/lalsimulation/_lalsimulation.so
%{py3_sitedir}/lalsimulation/*.py
%{py3_sitedir}/lalsimulation/__pycache__
%dir %{py3_sitedir}/lalsimulation/nrfits
%{py3_sitedir}/lalsimulation/nrfits/*.py
%{py3_sitedir}/lalsimulation/nrfits/__pycache__
%dir %{py3_sitedir}/lalsimulation/tilts_at_infinity
%{py3_sitedir}/lalsimulation/tilts_at_infinity/*.py
%{py3_sitedir}/lalsimulation/tilts_at_infinity/__pycache__
