%% Machine Learning for Economic Analysis
% Lecture 2: IV
% Prof: Damian Kozbur
% TA: Matteo Courthoud

%{

In this lecture we are going to simulate data for IV regression, compute
the IV estimator and it standard error. We are further going to examine
its asymtptotic properties.

%}

% Set seed
rng(123)

% Set the dimension of Z
l = 3;

% Draw instruments
Z = randn(n,l);

% Correlation matrix for error terms
S = eye(2,2); S(1,2)=.8; S(2,1)=.8; 

% Endogenous X
gamma = [2, 0; 0, -1; -1, 3];
e = randn(n,2)*chol(S);
X = Z*gamma + e(:,1);

% Calculate Y
Y = X*b + e(:,2);

% Estimate beta OLS
beta_OLS = (X'*X)\(X'*Y) % = 2.1957, -0.9022

% IV: l=k=2 instruments
Z_IV = Z(:,1:k);
beta_IV = (Z_IV'*X)\(Z_IV'*Y) % = 2.1207, -1.3617

% Calculate standard errors
ehat = Y - X*beta_IV;
V_NHC_IV = var(ehat) * inv(Z_IV'*X)*Z_IV'*Z_IV*inv(Z_IV'*X);
V_HC0_IV = inv(Z_IV'*X)*Z_IV' * diag(ehat.^2) * Z_IV*inv(Z_IV'*X);

% 2SLS: l=3 instruments
Pz = Z*inv(Z'*Z)*Z';
beta_2SLS = (X'*Pz*X)\(X'*Pz*Y) % = 2.0723, -0.9628

% Calculate standard errors
ehat = Y - X*beta_2SLS;
V_NCH_2SLS = var(ehat) * inv(X'*Pz*X);
V_HC0_2SLS = inv(X'*Pz*X)*X'*Pz * diag(ehat.^2) *Pz*X*inv(X'*Pz*X);

% GMM 1-step: inefficient weighting matrix
W_1 = eye(l);

% Objective function
gmm_1 = @(b) ( Y - X*b )' * Z * W_1 *  Z' * ( Y - X*b );

% Estimate GMM
beta_gmm_1 = fminsearch(gmm_1, beta_OLS) % = 2.0763, -0.9548
ehat = Y - X*beta_gmm_1;

% Standard errors GMM
S_hat = Z'*diag(ehat.^2)*Z;
d_hat = -X'*Z;
V_gmm_1 = inv(d_hat * inv(S_hat) * d_hat');

% GMM 2-step: efficient weighting matrix
W_2 = inv(S_hat);
gmm_2 = @(b) ( Y - X*b )' * Z * W_2 *  Z' * ( Y - X*b );
beta_gmm_2 = fminsearch(gmm_2, beta_OLS) % = 2.0595, -0.9666

% Standard errors GMM
ehat = Y - X*beta_gmm_2;
S_hat = Z'*diag(ehat.^2)*Z;
d_hat = -X'*Z;
V_gmm_2 = inv(d_hat * inv(S_hat) * d_hat');
