%% Machine Learning for Economic Analysis
% Lecture 1: OLS
% Prof: Damian Kozbur
% TA: Matteo Courthoud

%{

In this lecture we are going to simulate data for OLS regression, compute
the OLS estimator and it standard error. We are further going to examine
its asymtptotic properties.

%}

% Set seed
rng(123)

% Set the number of observations
n = 100;

% Set the dimension of X
k = 2;

% Draw a sample of explanatory variables
X = rand(n, k);

% Draw the error term
sigma = 1;
e = randn(n,1)*sqrt(sigma);

% Set the parameters
b = [2; -1];

% Calculate the dependent variable
Y = X*b + e;

% Estimate beta
b_hat = inv(X'*X)*(X'*Y) % = 1.9020, -0.9305

% Equivalent but faster formulation
b_hat = (X'*X)\(X'*Y);

% Even faster (but less intuitive) formulation
b_hat = X\Y;

% Note that is generally not equivalent to Var(X)^-1 * Cov(X,y)...
Var_X = cov(X);
Cov_Xy = n/(n-1) * (mean(X .* Y) - mean(X).*mean(Y));
b_alternative = inv(Var_X) * Cov_Xy' % = 2.1525, -0.7384

% ...unless you include a constant
a = 3;
Y = a + X*b + e;
b_hat_1 = [ones(n,1), X]\Y % = 2.1525, -0.7384
Var_X = cov(X);
Cov_Xy = n/(n-1) * (mean(X .* Y) - mean(X).*mean(Y));
b_alternative = inv(Var_X) * Cov_Xy' % = 2.1525, -0.7384

% Predicted y
y_hat = X*b_hat;

% Residuals
e_hat = Y - X*b_hat;

% Projection matrix
P = X*inv(X'*X)*X';

% Annihilator matrix
M = eye(n) - P;

% Leverage
h = diag(P);

% Biased variance estimator 
sigma_hat = e_hat'*e_hat / n;

% Unbiased estimator 1
sigma_hat_2 = e_hat'*e_hat / (n-k);

% Unbiased estimator 2
sigma_hat_3 = mean( e_hat.^2 ./ (1-h) );

% R squared - uncentered
R2_uc = (y_hat'*y_hat)/ (Y'*Y);

% R squared
y_bar = mean(Y);
R2 = ((y_hat-y_bar)'*(y_hat-y_bar))/ ((Y-y_bar)'*(Y-y_bar));

% Ideal variance of the OLS estimator
var_b = sigma*inv(X'*X);

% Standard errors
std_b = sqrt(diag(var_b));

% Set seed
rng(123)

% Homoskedastic standard errors
std_h = var(e_hat) * inv(X'*X);

% HC0 variance and standard errors
omega_hc0 = X' * diag(e_hat.^2) * X;
std_hc0 = sqrt(diag(inv(X'*X) * omega_hc0 * inv(X'*X))) % = 0.9195, 0.8631

% HC1 variance and standard errors
omega_hc1 = n/(n-k) * X' *  diag(e_hat.^2) * X;
std_hc1 = sqrt(diag(inv(X'*X) * omega_hc1 * inv(X'*X))) % = 0.9289, 0.8719

% HC2 variance and standard errors
omega_hc2 = X' * diag(e_hat.^2./(1-h)) * X;
std_hc2 = sqrt(diag(inv(X'*X) * omega_hc2 * inv(X'*X))) % = 0.9348, 0.8768

% HC3 variance and standard errors
omega_hc3 = X' * diag(e_hat.^2./(1-h).^2) * X;
std_hc3 = sqrt(diag(inv(X'*X) * omega_hc3 * inv(X'*X))) % = 0.9504, 0.8907

% Note what happens if you allow for full autocorrelation
omega_full = X'*e_hat*e_hat'*X;

% t-test for beta=0
t = abs(b_hat./(std_hc1));

% p-value
p_val = 1 - normcdf(t);

% F statistic of joint significance
SSR_u = e_hat'*e_hat;
SSR_r = Y'*Y;
F = (SSR_r - SSR_u)/k / (SSR_u/(n-k));

% 95% confidente intervals
conf_int = [b_hat - 1.96*std_hc1, b_hat + 1.96*std_hc1];


