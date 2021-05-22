from gurobipy import *

# REPRODUCE OF WORK 
# Evaluation of mixed integer programming formulations for non-preemptive parallel machine scheduling problems
# Section 3.5.1 MIP
# This work has some wrong, I add something by myself.



# in this case, from M1 to M6, has precedence constraints, different machine 
# from M6 back to M1, has precedence constraints , different machine 
#  M11 to M12 also need precedence constraints , same machine 


number_job = 10                            # number of jobs
number_machine = 3                         # number of machines
processing_time = [13,5,12,3,32,4,25,16,54,4]    # processing times of the jobs

plist= [[0,4],[3,5],[6,9],[4,7]]


# Initialize the gurobi model
m = Model()

# Add variables 
x = m.addVars(number_machine,number_job,vtype=GRB.BINARY, name='x')
C     = m.addVars(number_job, lb = 0, name='C')
delta = m.addVars(number_job,number_job,vtype=GRB.BINARY, name='delta')
y     = m.addVars(number_job,number_job,vtype=GRB.BINARY, name='y')
Cmax = m.addVar(lb = 0, name='makespan')



# Set the objective, i.e., the minimization of the makespan
m.setObjective(Cmax,GRB.MINIMIZE)

# Add constraints
for j in range(number_job):
    m.addConstr(C[j] <= Cmax)

# for i in range(number_machine):
#     m.addConstr(quicksum(x[i,j]*processing_time[j] for j in range(number_job)) <= C[i]) 

for j in range(number_job):
    m.addConstr(quicksum(x[i,j] for i in range(number_machine)) == 1) 

for i in range(number_machine):
    for t in range(number_job):
        for j in range(t+1, number_job):
            m.addConstr(x[i,t] + x[i,j] +y[t,j] <= 2)

for t in range(number_job):
    for j in range(t+1, number_job):
        m.addConstr(delta[t,j] + delta[j,t] + y[t,j] ==1)

for t in range(number_job):
    for j in range(t+1, number_job):
        for k in range(j+1, number_job):
            m.addConstr(delta[t,j] + delta[j,k] + delta[k,t] <=2)


for i in range(number_machine):
    for t in range(number_job):
        for j in range(number_job):
            m.addConstr(C[j] >= C[t] + processing_time[j]*(delta[t,j] + x[i,t] + x[i,j] -2)-1000*(1-delta[t,j]))

for i in range(number_machine):
    for j in range(number_job):
        m.addConstr(C[j] >= processing_time[j]* x[i,j])


for ll in plist:
    m.addConstr(delta[ll[0],ll[1]] == 1)
    m.addConstr(y[ll[0],ll[1]] == 0)
    m.addConstr(y[ll[1],ll[0]] == 0)

for ll in plist:
    for i in range(number_machine):
        m.addConstr(x[i, ll[0]] == x[i,ll[1]])




m.optimize()
m.write('lnear_model11.lp')

machine_list =[]
for i in range(number_machine):
    machine_list.append([])
for i in range(number_machine):
  for j in range(number_job):
    if(x[i,j].X == 1):
        machine_list[i].append(j)
        
print(machine_list)

for j in range(number_job):
    print(C[j].X)

for t in range(number_job):
  for j in range(number_job):
    if(y[t,j].X == 1):
        print('t',t,'j',j)