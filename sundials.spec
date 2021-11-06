%define	major 5
%define	libname		%mklibname %{name} %{major}
%define	develname	%mklibname %{name} -d

%bcond_with fortran
%bcond_without pthread

%if %{with pthread}
%define _disable_ld_no_undefined 1
%endif

Summary:	SUite of Nonlinear and DIfferential/ALgebraic Equation Solvers
Name:		sundials
Version:	5.8.0
Release:	1
License:	BSD
Group:		Sciences/Computer science
URL:		https://computation.llnl.gov/projects/%{name}
Source0:	https://github.com/LLNL/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:	cmake
BuildRequires:	ninja
%if %{with fortran}
BuildRequires:	gcc-gfortran
%endif
BuildRequires:	blas-devel
BuildRequires:	lapack-devel
BuildRequires:	libgomp-devel
BuildRequires:	openmpi-devel
%ifarch %{ix86} x86_64
BuildRequires:	quadmath-devel
%endif
BuildRequires:	suitesparse-devel

Requires:	%{libname} = %{version}-%{release}

%description
SUNDIALS is a SUite of Nonlinear and DIfferential/ALgebraic equation
Solvers. It consists of the following six solvers:
  - CVODE solves initial value problems for ordinary differential
          equation (ODE) systems;
  - CVODES solves ODE systems and includes sensitivity analysis
           capabilities (forward and adjoint);
  - ARKODE solves initial value ODE problems with additive
           Runge-Kutta methods, include support for IMEX methods;
  - IDA solves initial value problems for differential-algebraic
        equation (DAE) systems;
  - IDAS solves DAE systems and includes sensitivity analysis
         capabilities (forward and adjoint); 
  - KINSOL solves nonlinear algebraic systems.

%files
%doc LICENSE README.md
#{_docdir}/sundials
%{_datadir}/%{name}/examples

#-----------------------------------------------------------------------------

%package -n %{libname}
Summary:	SUite of Nonlinear and DIfferential/ALgebraic Equation Solvers
Group:		System/Libraries

%description -n %{libname}
SUNDIALS is a SUite of Nonlinear and DIfferential/ALgebraic equation
Solvers. It consists of the following six solvers:
  - CVODE solves initial value problems for ordinary differential
          equation (ODE) systems;
  - CVODES solves ODE systems and includes sensitivity analysis
           capabilities (forward and adjoint);
  - ARKODE solves initial value ODE problems with additive
           Runge-Kutta methods, include support for IMEX methods;
  - IDA solves initial value problems for differential-algebraic
        equation (DAE) systems;
  - IDAS solves DAE systems and includes sensitivity analysis
         capabilities (forward and adjoint); 
  - KINSOL solves nonlinear algebraic systems.

%files -n %{libname}
%{_libdir}/*.so.*

#-----------------------------------------------------------------------------

%package -n %{develname}
Summary:	Development files for the SUNDIALS libraries
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}

%description -n %{develname}
This package contains development files for %{name}.

%files -n %{develname}
%{_includedir}/*/*.h
%{_includedir}/%{name}/NOTICE
%{_libdir}/lib%{name}_*.so
%{_libdir}/cmake/%{name}/*.cmake
%if %{with fortran}
%{fincludedir}/*.mod
%endif

#-----------------------------------------------------------------------------

%prep
%setup -q
%autopatch -p1

#if %{with fortran}
#export CC=gcc
#export CXX=g++
#endif

%cmake \
	-DBUILD_STATIC_LIBS:BOOL=OFF \
%if %{with fortran}
	-DBUILD_FORTRAN77_INTERFACE:BOOL=OFF \
	-DBUILD_FORTRAN_MODULE_INTERFACE:BOOL=ON \
	-DFortran_INSTALL_MODDIR:PATH=%{fincludedir} \
%endif
	-DENABLE_MPI:BOOL=OFF \
	-DENABLE_OPENMP:BOOL=ON \
%if %{with pthread}
	-DENABLE_PTHREAD:BOOL=ON \
%else
	-DENABLE_PTHREAD:BOOL=OFF \
%endif
	-DENABLE_CUDA:BOOL=OFF \
	-DENABLE_LAPACK:BOOL=ON \
	-DENABLE_KLU:BOOL=ON \
	-DKLU_INCLUDE_DIR:PATH=%{_includedir}/suitesparse \
	-DKLU_LIBRARY_DIR:PATH=%{_libdir} \
	-DEXAMPLES_INSTALL_PATH:PATH=%{_datadir}/%{name}/examples \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build

rm %{buildroot}%{_includedir}/sundials/LICENSE

