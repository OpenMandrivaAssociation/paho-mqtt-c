%define major 1
%define libname %mklibname paho-mqtt
%define devname %mklibname paho-mqtt -d

%bcond_with	tests

Summary:	Eclipse Paho C client library for MQTT
Name:		paho-mqtt-c
Version:	1.3.13
Release:	1
License:	BSD and EPL
URL:		https://eclipse.org/paho/clients/c/
Source0:	https://github.com/eclipse/paho.mqtt.c/archive/v%{version}/paho.mqtt.c-%{version}.tar.gz
#Source1:	unused.abignore

BuildRequires:	cmake
BuildRequires:	graphviz
BuildRequires:	doxygen
BuildRequires:	pkgconfig(openssl)

%description
The Paho MQTT C Client is a fully fledged MQTT client written in C.

%files
%{_bindir}/paho*
#{_datadir}/%{name}/abi/paho-c.abignore

#---------------------------------------------------------------------------

%package -n %{libname}
Summary:	Eclipse Paho C client library for MQTT
License:	BSD and EPL
Group:		System/Libraries

%description -n %{libname}
The Paho MQTT C Client is a fully fledged MQTT client written in C.

%files -n %{libname}
%{_libdir}/libpaho-mqtt*.so.%{major}*

#---------------------------------------------------------------------------

%package -n %{devname}
Summary:	MQTT C Client development kit
License:	BSD and EPL
Group:		System/Libraries
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}
Provides:	lib%{name}-devel = %{version}

%description -n %{devname}
Development files and samples for the the Paho MQTT C Client.

%files -n %{devname}
%license LICENSE edl-v10 epl-v20
%doc CONTRIBUTING.md README.md notice.html
%doc %{_docdir}/%{devname}/MQTTAsync
%doc %{_docdir}/%{devname}/MQTTClient
%doc %{_docdir}/%{devname}/MQTTClient_internal
%doc %{_docdir}/%{devname}/samples
%{_bindir}/MQTT*
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/cmake/eclipse-paho-mqtt-c/
%{_mandir}/man3/*

#---------------------------------------------------------------------------

%prep
%autosetup -n paho.mqtt.c-%{version}

%build
%cmake \
	-DPAHO_WITH_SSL:BOOL=ON \
	-DPAHO_BUILD_DOCUMENTATION:BOOL=ON \
	-DPAHO_BUILD_SAMPLES:BOOL=ON \
	-DPAHO_ENABLE_CPACK:BOOL=ON \
	-GNinja
%ninja_build

%install
%ninja_install -C build

#install -D -p -m 755 %{SOURCE0} %{buildroot}%{_datadir}/%{name}/abi/paho-c.abignore

# fix man path
install -dm 0755 %{buildroot}%{_mandir}/man3
for f in MQTTAsync MQTTClient
do
	mv -f %{buildroot}%{_docdir}/Eclipse\ Paho\ C/$f/man/man3/* %{buildroot}%{_mandir}/man3/
	rm -rf %{buildroot}%{_docdir}/Eclipse\ Paho\ C/$f/man
done

# fix doc path
install -dm 0755 %{buildroot}%{_docdir}/%{devname}
for f in MQTTAsync MQTTClient MQTTClient_internal samples
do
	mv -f %{buildroot}%{_docdir}/Eclipse\ Paho\ C/$f %{buildroot}%{_docdir}/%{devname}/
done
rm -fr %{buildroot}%{_docdir}/Eclipse\ Paho\ C/

%check
%if %{with tests}
export LD_LIBRARY_PATH=.
%ninja_test -C build
%endif

