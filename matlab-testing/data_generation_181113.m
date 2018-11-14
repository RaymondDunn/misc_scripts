% data_generation_181113
%% params
num_datapoints = 30;

% make opto on/opto off data
arr = cat(2, zeros(1,num_datapoints), ones(1,num_datapoints));
perm = randperm(length(arr));
opto_on = arr(perm);


%% make reaction times from gaussians centered
% combine with randperm indexes
% opto off has reaction time of ~5s
mu = 5;
rts_short = normrnd(mu, sqrt(mu), 1, num_datapoints);

% opto on has reaction time of ~11s
mu = 11;
rts_long = normrnd(mu, sqrt(mu), 1, num_datapoints);
rts = cat(2, rts_short, rts_long);
reaction_times = rts(perm);


%% make left/right decisions, random
arr = cat(2, zeros(1,num_datapoints), ones(1,num_datapoints));
direction_decided = arr(randperm(length(arr)));


%% make correct or not
% again shuffle according to opto indexes
% opto off gets 0.6 correct
correct_perc = 0.6;
correct_hits = floor(num_datapoints * correct_perc);
correct = cat(2, ones(1, correct_hits), zeros(1, 2*num_datapoints - correct_hits));
correct_low = correct(randperm(length(correct)));

% opto on gets 0.71 correct
correct_perc = 0.71;
correct_hits = floor(num_datapoints * correct_perc);
correct = cat(2, ones(1, correct_hits), zeros(1, 2*num_datapoints - correct_hits));
correct_high = correct(randperm(length(correct)));

correct = cat(2, correct_low, correct_high);
correct = correct(perm);


%% assemble into struct
mouse1_data.reaction_times = reaction_times;
mouse1_data.opto_on = opto_on;
mouse1_data.correct_decision = correct;
mouse1_data.direction_decided = direction_decided;

% save
save('mouse1_data.mat', 'mouse1_data') 
