#
# Conditional build:
%bcond_without	apidocs	# API documentation
%bcond_without	python	# Python binding
#
Summary:	Trace Format Babel Tower
Summary(pl.UTF-8):	Wieża Babel formatów narzędzi śledzących
Name:		babeltrace2
Version:	2.0.3
Release:	2
License:	MIT
Group:		Applications/System
Source0:	https://www.efficios.com/files/babeltrace/%{name}-%{version}.tar.bz2
# Source0-md5:	9a8f40ddc18dac6c11af9a3fd0207feb
Patch0:		%{name}-python.patch
URL:		https://babeltrace.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.12
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	elfutils-devel >= 0.154
BuildRequires:	glib2-devel >= 1:2.28.0
BuildRequires:	libtool >= 2:2
BuildRequires:	libuuid-devel
BuildRequires:	pkgconfig
BuildRequires:	popt-devel
%{?with_python:BuildRequires:	python3-devel >= 1:3.2}
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.507
BuildRequires:	swig-python >= 2.0.0
Requires:	elfutils >= 0.154
Requires:	glib2 >= 1:2.28.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This project provides trace read and write libraries, as well as a
trace converter. A plugin can be created for any trace format to allow
its conversion to/from another trace format.

%description -l pl.UTF-8
Ten projekt udostępnia biblioteki do odczytu i zapisu śladów, a także
konwerter śladów. Można tworzyć wtyczki dla dowolnego formatu śladów,
aby umożliwić konwersję do/z innego formatu.

%package devel
Summary:	Header files for Babeltrace libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek Babeltrace
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	elfutils-devel >= 0.154
Requires:	glib2-devel >= 1:2.28.0
Requires:	libuuid-devel
Requires:	popt-devel

%description devel
Header files for Babeltrace libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek Babeltrace.

%package static
Summary:	Static Babeltrace 2 libraries
Summary(pl.UTF-8):	Statyczne biblioteki Babeltrace 2
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Babeltrace 2 libraries.

%description static -l pl.UTF-8
Statyczne biblioteki Babeltrace 2.

%package apidocs
Summary:	API documentation for Babeltrace 2 libraries
Summary(pl.UTF-8):	Dokumentacja API bibliotek Babeltrace 2
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Babeltrace 2 libraries.

%description apidocs -l pl.UTF-8
Dokumentacja API bibliotek Babeltrace 2.

%package -n python3-babeltrace2
Summary:	Python 3 binding to Babeltrace 2 library
Summary(pl.UTF-8):	Wiązanie Pythona 3 do biblioteki Babeltrace 2
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python3-babeltrace2
Python 3 binding to Babeltrace 2 library.

%description -n python3-babeltrace2 -l pl.UTF-8
Wiązanie Pythona 3 do biblioteki Babeltrace 2.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_apidocs:--enable-api-doc} \
	%{?with_python:--enable-python-bindings} \
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/babeltrace2/plugins/*.{la,a}
# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/babeltrace2

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog LICENSE README.adoc mit-license.txt std-ext-lib.txt
%attr(755,root,root) %{_bindir}/babeltrace2
%attr(755,root,root) %{_libdir}/libbabeltrace2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbabeltrace2.so.0
%attr(755,root,root) %{_libdir}/libbabeltrace2-ctf-writer.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbabeltrace2-ctf-writer.so.0
%dir %{_libdir}/babeltrace2
%dir %{_libdir}/babeltrace2/plugins
%attr(755,root,root) %{_libdir}/babeltrace2/plugins/babeltrace-plugin-ctf.so
%attr(755,root,root) %{_libdir}/babeltrace2/plugins/babeltrace-plugin-lttng-utils.so
%attr(755,root,root) %{_libdir}/babeltrace2/plugins/babeltrace-plugin-text.so
%attr(755,root,root) %{_libdir}/babeltrace2/plugins/babeltrace-plugin-utils.so
%{_mandir}/man1/babeltrace2.1*
%{_mandir}/man1/babeltrace2-convert.1*
%{_mandir}/man1/babeltrace2-help.1*
%{_mandir}/man1/babeltrace2-list-plugins.1*
%{_mandir}/man1/babeltrace2-query.1*
%{_mandir}/man1/babeltrace2-run.1*
%{_mandir}/man7/babeltrace2*.7*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbabeltrace2.so
%attr(755,root,root) %{_libdir}/libbabeltrace2-ctf-writer.so
%{_includedir}/babeltrace2
%{_includedir}/babeltrace2-ctf-writer
%{_pkgconfigdir}/babeltrace2.pc
%{_pkgconfigdir}/babeltrace2-ctf-writer.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libbabeltrace2.a
%{_libdir}/libbabeltrace2-ctf-writer.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/api/libbabeltrace2/output/html/{search,*.css,*.html,*.js,*.png}
%endif

%if %{with python}
%files -n python3-babeltrace2
%defattr(644,root,root,755)
%dir %{py3_sitedir}/bt2
%attr(755,root,root) %{py3_sitedir}/bt2/_native_bt.cpython-*.so
%{py3_sitedir}/bt2/*.py
%{py3_sitedir}/bt2/__pycache__
%{py3_sitedir}/bt2-%{version}-py*.egg-info
%endif
