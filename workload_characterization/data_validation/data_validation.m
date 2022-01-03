clear; clc; close all;
ll_realistic = readtable("realistic_ll.csv");
ll_synthetic = readtable("synthetic_ll.csv");
first_col = 25;
last_col = 37;
ll_realistic = str2double(table2array(ll_realistic(:, first_col:last_col)));
ll_synthetic = str2double(table2array(ll_synthetic(:, first_col:last_col)));
[~, n] = size(ll_realistic);
results = ones(1, n); % data validation wants them to be all zeros
p_values = zeros(1, n);

figure;
qqplot(ll_realistic - ll_synthetic);

figure();
subplot(2,1,1);
boxplot(ll_realistic,'Whisker',100);
subplot(2,1,2)
boxplot(ll_synthetic,'Whisker',100);


% visual tests
% for i=1:n
%     x = ll_realistic(:, i);
%     y = ll_synthetic(:, i);
%     figure(2*i);
%     qqplot(x - y);
%     figure(2*i + 1);
%     boxplot([x, y]);
% end


not_eq_var_vect = zeros(1, n); % this vector should be filled manually based on visual tests
% not_eq_var_vect(1) = 1;
% not_eq_var_vect(2) = 1;
% not_eq_var_vect(6) = 1;
% not_eq_var_vect(7) = 1;
% not_eq_var_vect(8) = 1;
% not_eq_var_vect(10) = 1;
% not_eq_var_vect(11) = 1;
% not_eq_var_vect(12) = 1;
% not_eq_var_vect(13) = 1;
% not_eq_var_vect(14) = 1;

[not_normal, p_ks] = kstest(ll_realistic - ll_synthetic);
%not_normal = 0;

for i=1:n
    x = ll_realistic(:, i);
    y = ll_synthetic(:, i);
    if not_normal == 1
        [p, h] = ranksum(x, y);
    else
        not_eq_var = vartest2(x, y);
        if not_eq_var_vect(i) ~= not_eq_var
            fprintf("vartest2 for column %d not according with visual test\n", i);
        end
        if not_eq_var_vect(i) == 1
            [h, p] = ttest2(x, y, 'Vartype', 'unequal');
        else
            [h, p] = ttest2(x, y);
        end
    end
    results(i) = h;
    p_values(i) = p;
end

