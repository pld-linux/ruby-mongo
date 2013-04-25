#
# Conditional build:
%bcond_without	tests		# build without tests

%define	gem_name mongo
Summary:	Ruby driver for the MongoDB
Name:		ruby-%{gem_name}
Version:	1.6.4
Release:	1
License:	Apache v2.0
Group:		Development/Languages
Source0:	http://rubygems.org/gems/%{gem_name}-%{version}.gem
# Source0-md5:	c483d7ae303c5ea4d41ea7556b4a1917
URL:		http://www.mongodb.org
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.656
%if %{with tests}
BuildRequires:	ruby-bson
#BuildRequires: ruby-minitest
BuildRequires:	ruby-mocha
BuildRequires:	ruby-shoulda
BuildRequires:	ruby-test-unit
%endif
Requires:	ruby-bson = %{version}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A Ruby driver for MongoDB. For more information about Mongo, see
<http://www.mongodb.org>.

%package doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description doc
Documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version}

%build
%if %{with tests}
# Most tests require a mongo server to be running
# We are only running tests that do not require the server
RUBYOPT="-rdate" testrb \
	test/conversions_test.rb \
	test/support_test.rb \
	test/uri_test.rb \
	test/unit/*_test.rb
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{_bindir}}
cp -a bin/* $RPM_BUILD_ROOT%{_bindir}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md LICENSE.txt
%attr(755,root,root) %{_bindir}/mongo_console
%{ruby_vendorlibdir}/mongo.rb
%{ruby_vendorlibdir}/mongo
