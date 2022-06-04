disp("compiling mex function ...")
mex forward.c -DMATLAB_MEX_FILE

disp("loading test data ...")
data = load("forward_data.mat");

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