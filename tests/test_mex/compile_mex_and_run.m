args = argv();

c_file = sprintf("%s.c", args{1});
data_file = sprintf("%s.mat", args{1});

fprintf("compiling %s and testing with %s\n", c_file, data_file)
disp("compiling mex function ...")
cmd_str = sprintf("mex %s -DMATLAB_MEX_FILE", c_file);
eval(cmd_str);

disp("loading test data ...")
data = load(data_file);

disp("executing model with test data ...")
[states_dot, outputs, con_outputs, residuals] = forward(data.states, data.inputs, data.mesh, data.params);

disp("check results against test data ...")
% Check results, pay attention to the transpose as python is row major

disp("checking states_dot ...")
assert(states_dot, data.states_dot')

disp("checking outputs ...")
assert(outputs, data.outputs')
% assert(con_outputs, data.con_outputs') % don't compare because it's empty

disp("checking residuals ...")
assert(residuals, data.residuals')