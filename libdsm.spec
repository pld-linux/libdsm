#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Minimalist and read-only SMB client library
Summary(pl.UTF-8):	Minimalistyczna biblioteka klienta SMB (tylko do odczytu)
Name:		libdsm
Version:	0.3.1
Release:	1
License:	LGPL v2.1+ or commercial
Group:		Libraries
#Source0Download: https://github.com/videolabs/libdsm/releases
Source0:	https://github.com/videolabs/libdsm/releases/download/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	1dd8c11c1726d5afb33183ce71e12372
URL:		https://videolabs.github.io/libdsm/
#BuildRequires:	autoconf >= 2.53
#BuildRequires:	automake >= 1:1.6
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	libbsd-devel
BuildRequires:	libtasn1-devel >= 3.0
#BuildRequires:	libtool >= 2:2
Requires:	libtasn1 >= 3.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
lib Defective SMb (libDSM) is a SMB protocol client implementation in
pure old C, with a lot less features than Samba but with a much
simpler, and a more permissive license (currently LGPL + proprietary).

%description -l pl.UTF-8
lib Defective SMb (libDSM) to implementacja klienta protokołu SMB w
czystym, starym C. Ma o wiele mniej możliwości niż Samba, ale jest
dużo prostsza i ma luźniejszą licencję (obecnie LGPL z opcją
komercyjną).

%package devel
Summary:	Header files for liBDSM library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki liBDSM
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libtasn1-devel >= 3.0

%description devel
Header files for liBDSM library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki liBDSM.

%package static
Summary:	Static liBDSM library
Summary(pl.UTF-8):	Statyczna biblioteka liBDSM
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static liBDSM library.

%description static -l pl.UTF-8
Statyczna biblioteka liBDSM.

%package apidocs
Summary:	API documentation for liBDSM library
Summary(pl.UTF-8):	Dokumentacja API biblioteki liBDSM
Group:		Documentation

%description apidocs
API documentation for liBDSM library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki liBDSM.

%prep
%setup -q

%{__sed} -ne '1,/^===/ p' COPYING > LICENSE

%build
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}
%{__make}

%if %{with apidocs}
%{__make} doc
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkgconfig
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libdsm.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE NEWS
%attr(755,root,root) %{_bindir}/dsm
%attr(755,root,root) %{_bindir}/dsm_discover
%attr(755,root,root) %{_bindir}/dsm_inverse
%attr(755,root,root) %{_bindir}/dsm_lookup
%attr(755,root,root) %{_libdir}/libdsm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdsm.so.3

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdsm.so
%{_includedir}/bdsm
%{_pkgconfigdir}/libdsm.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libdsm.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/html/*
%endif
