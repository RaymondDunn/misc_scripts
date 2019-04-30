function [L,k,b]=fitGLM_template(Spikes,X,fname)
    % INPUTS
    % Spikes:   row vector of length N with numbers of spikes at each time step
    % X:        raw (unfiltered) input. Matrix with dimensions DxN where D is
    %           the dimension of the input
    % fname:    a string indicating the nonlinearity to use 'quad', 'smooth', or 'exp'
    %
    % OUTPUTS
    % L:        row vector of loglikelihoods at every iteration of Newton-Raphson
    % k:        input filter coefficients (dimensionless)
    % b:        background firing rate Hz
    
    %% Some initialization
    % Choice of nonlinearity and its derivatives
    switch fname
        case 'exp'
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            % the exponential and its derivatives and inverse
            'your code goes here';
            f = @exp;
            df = @exp;
            d2f = @exp;
            invf = @log;
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        case 'smooth'
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            % the smooth rectified linear and its derivatives and inverse
            'your code goes here';
            % f=
            % df=
            % d2f=
            % invf= This one isn't technically needed, but it's nice to have for initialization of b (see below)
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        case 'quad'
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            % the rectified quadratic and its derivatives and inverse
            'your code goes here';
            % f=
            % df=
            % d2f=
            % invf= This one isn't technically needed, but it's nice to have for initialization of b (see below)
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    end
    
    % lines for local testing
    Spikes = Spikes_train;
    X = X_train;
    
    % Time step size
    dt=.001; % seconds
    
    % Tolerance for convergence
    tol=1e-7;
    
    % A good initialization for k is the mean of X at spike times
    k=mean(X(1:end,Spikes~=0),2);
    
    % A good initialization for b is the total average firing rate
    b=sum(Spikes)/(dt*length(Spikes));
    
    % Augment X with 1's so we maximize k and b together
    X=[X;ones(1,size(X,2))];
    
    % Invert f to augument k with b
    k=[k;invf(b)]; % Only if you know invf
    %k=[k;1]; % Or try this one

    % So we can watch k evolve...
    fig=figure;
    img=imagesc(reshape(k(1:end-1),7,7));
    
    % Initialize L at -inf
    L=-inf*ones(1,1000);
    
    % Nonzero spike times (you'll want this!)
    nz=Spikes>0;
    total_t = 200000;
    
    % Loop until Newton-Raphson converges
    j=1;
    k_old=k;
    while true
        j=j+1;
        
        % Trick to deal with bad Newton steps
        k=2*k-k_old; % initialize k such that when we take the mean in 2 lines it's the correct value
        while ~isfinite(L(j))
            k=.5*(k+k_old); % move k back toward k_old
    
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            % Calculate log-likelihood (you can ignore the constant terms here if you want)
            ll = 0;
            for t = 1:total_t
                lambda_t = f(dot(k, X(:,t)) + b);
                yt = Spikes(t);
                d_spikes = dt * lambda_t;
                ll = ll + log((d_spikes^yt * exp(-d_spikes))/factorial(yt));
                if mod(t, 20000) == 0
                    disp(t)
                end
            end
            L(j) = ll;
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        end
        
        % Plot k
        set(img,'CData',reshape(k(1:end-1),7,7));
        drawnow;

        % Calculate the size of the error
        delta=abs((L(j)-L(j-1))/L(j));
        
        % Print iteration information
        fprintf('iter: %d, LL: %g, delta: %g\n',j-1,L(j),delta);
        
        % Convergence criteria
        if delta < tol
            break;
        end
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % Calculate gradient
        'your code goes here';
        % g=
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % Calculate Hessian
        'your code goes here';
        % H=
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % Newton-Raphson
        k_old=k;
        'your code goes here';
        % k=
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    end
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Deal the outputs
    L=L(1:j);
    'your code goes here';
    % b=
    % k=
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    % Close the figure
    close(fig);
end