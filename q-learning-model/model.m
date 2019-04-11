% load probabilities
prob_rwd_1 = csvread('prob_rwd_1.csv');
prob_rwd_2 = csvread('prob_rwd_2.csv');

% vars for qs/outputs
qs_1 = zeros(size(prob_rwd_1));
qs_2 = zeros(size(prob_rwd_2));

% initialize
qs_1(1) = 0.5;
qs_2(1) = 0.5;
a = 0.2;
b = 3;
num_trials = 361;

% iterate trials
for i = 1:num_trials
    
    % get qs
    q1 = qs_1(i);
    q2 = qs_2(i);
    
    % calculate probabilities of choosing
    prob_choice_1 = 1 / (1 + exp(-b(q1-q2)))
    prob_choice_2 = 1 - prob_choice_0;
    
    % get p_reward
    if prob_choice_1 >= prob_choice_2
        p_reward = prob_rwd_1(i);
        
    else
        p_reward = prob_rwd_2(i);
    end
    
    % 
    
    % update rpe
end


function lol = calculate_choice(beta, q1, q2)
    lol = 1
end

function 
