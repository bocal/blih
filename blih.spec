#-
# Copyright 2013-2014 Emmanuel Vadot <elbarto@bocal.org>
# All rights reserved
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted providing that the following conditions 
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

Name:           blih
Version:        1.7
Release:        1
License:        BSD-2-Clause
Summary:        Bocal Lightweight Interface for Humans
BuildRequires:  python3
BuildArch:      noarch
Source0:        http://pkg.bocal.org/pub/%{name}/%{version}/%{name}-%{version}.tgz
Vendor:         Bocal
Url:            http://www.bocal.org
Group:          Applications/Internet
Packager:       Emmanuel Vadot <elbarto@bocal.org>

%description
Bocal Lightweight Interface for Humans
Python script for the BLIH API

%prep
%setup

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
cp blih.py %{buildroot}%{_bindir}/blih;

%files
%attr(755,root,root) %{_bindir}/blih

%changelog
* Fri Feb 28 2014 Emmanuel Vadot <elbarto@bocal.org> - 1.7-1
- change arch to noarch
- change licence to BSD-2-Clause
- 