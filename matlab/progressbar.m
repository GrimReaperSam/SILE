function mem = progressbar(mem, i, max)

T_REFRESH = 1; % time until status is refreshed
bar = '                   |'; % empty progress bar

% initialize
if i == 1
    mem = zeros(4, 1, 'uint64'); % "memory" vriable with important data for progress bar
	mem(1) = tic; % time stamp from first iteration
    mem(2) = 0; % number of characters of last string
    mem(3) = tic; % time stamp from last refresh
    mem(4) = 1; % i from last refresh
elseif toc(mem(3)) > T_REFRESH
    
    % clean up old stuff
    for k = 1:double(mem(2))
        fprintf('\b');
    end
    
    % assemble progress bar
    state = floor(i/max*length(bar));
    for k = 1:state
        bar(k) = '*';
    end
        
    % new status info
    p = 100*i/max;
    t_avg = toc(mem(3))/(i-double(mem(4)));
    t_avg_tot = toc(mem(1))/i;
    t_tot = toc(mem(1));
    t_rem = (max-i)*t_avg_tot;
    
    t_avg = time2str(t_avg);
    t_avg_tot = time2str(t_avg_tot);
    t_tot = time2str(t_tot);
    t_rem = time2str(t_rem);
    
    % assemble status info
    status = sprintf(' i=%.0f, p=%3.1f%%, avg=%s, avg_tot=%s, tot=%s, rem=%s     ', i, p, t_avg, t_avg_tot, t_tot, t_rem);
    fprintf('%s%s', bar, status);
    
    % update memory
    mem(2) = length(bar) + length(status);
	mem(3) = tic;
	mem(4) = i;
end

% finish
if i == max
    for k = 1:double(mem(2))
        fprintf('\b');
    end
    avg = time2str(toc(mem(1))/max);
    tot = time2str(toc(mem(1)));
    fprintf('iter=%.0f, avg=%s, tot=%s\n', max, avg, tot);
end



function str = time2str(time)
if time < 1e-3
    str = sprintf('%.0fus', round(1e6*time));
elseif time < 1
    str = sprintf('%.0fms', round(1000*time));
elseif time < 60
    str = sprintf('%.1fs', round(time));
elseif time < 3600
    str = sprintf('%.0fm%.0fs', floor(time/60), round(mod(time, 60)));
elseif time < 86400
    time = round(time/60);
    str = sprintf('%.0fh%.0fm', floor(time/60), round(mod(time, 60)));
else
    time = round(time/3600);
    str = sprintf('%.0fd%.0fh', floor(time/24), round(mod(time, 24)));
end
