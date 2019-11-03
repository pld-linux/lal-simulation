#
# Conditional build:
%bcond_without	openmp	# OpenMP support
#
Summary:	LAL Simulation library
Summary(pl.UTF-8):	Biblioteka LAL Simulation
Name:		lal-simulation
Version:	1.9.1
Release:	1
License:	GPL v2+
Group:		Libraries
Source0:	http://software.ligo.org/lscsoft/source/lalsuite/lalsimulation-%{version}.tar.xz
# Source0-md5:	0a963ccea2b38e0168a845eda49cccf9
Patch0:		%{name}-env.patch
Patch1:		no-Werror.patch
URL:		https://wiki.ligo.org/DASWG/LALSuite
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
BuildRequires:	gsl-devel >= 1.13
BuildRequires:	lal-devel >= 6.18.0
%{?with_openmp:BuildRequires:	libgomp-devel}
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	octave-devel >= 1:3.2.0
BuildRequires:	pkgconfig
BuildRequires:	python-devel >= 1:2.6
BuildRequires:	python-numpy-devel >= 1:1.7
BuildRequires:	swig >= 3.0.12
BuildRequires:	swig-python >= 2.0.12
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires:	gsl >= 1.13
Requires:	lal >= 6.18.0
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
Requires:	lal-devel >= 6.18.0

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
Requires:	octave-lal >= 6.18.0

%description -n octave-lalsimulation
Octave interface for LAL Simulation.

%description -n octave-lalsimulation -l pl.UTF-8
Interfejs Octave do biblioteki LAL Simulation.

%package -n python-lalsimulation
Summary:	Python bindings for LAL Simulation
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki LAL Simulation
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python-lal >= 6.18.0
Requires:	python-modules >= 1:2.6

%description -n python-lalsimulation
Python bindings for LAL Simulation.

%description -n python-lalsimulation -l pl.UTF-8
Wiązania Pythona do biblioteki LAL Simulation.

%prep
%setup -q -n lalsimulation-%{version}
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal} -I gnuscripts
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_openmp:--disable-openmp} \
	--enable-swig
%{__make} V=1

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
%attr(755,root,root) %ghost %{_libdir}/liblalsimulation.so.20
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

%files -n python-lalsimulation
%defattr(644,root,root,755)
%dir %{py_sitedir}/lalsimulation
%attr(755,root,root) %{py_sitedir}/lalsimulation/_lalsimulation.so
%{py_sitedir}/lalsimulation/*.py[co]
