from gurobipy import *


# This MIP reproduce work
# A heuristic serial schedule algorithm for unrelated parallel machine scheduling with precedence constraints
# section 2
# This precedence constraints is strict


number_job = 10                            # number of jobs
number_machine = 3                         # number of machines
processing_time = [13,5,12,3,32,4,25,16,54,4]    # processing times of the jobs

UB = number_job-number_machine+1

plist= [[],[],[],[],[0],[3],[],[4],[],[6]]


# Initialize the gurobi model
m = Model()

# Add variables 
x = m.addVars(number_machine,number_job,number_job, vtype=GRB.BINARY, name='x')
C     = m.addVars(number_job, lb = 0, name='C')
# delta = m.addVars(number_job,number_job,vtype=GRB.BINARY, name='delta')
# y     = m.addVars(number_job,number_job,vtype=GRB.BINARY, name='y')
Cmax = m.addVar(lb = 0, name='makespan')



# Set the objective, i.e., the minimization of the makespan
m.setObjective(Cmax,GRB.MINIMIZE)

for j in range(number_job):
    m.addConstr(quicksum(x[i,j,k] for i in range(number_machine) for k in range(UB)) == 1)

for k in range(UB):
    for i in range(number_machine):
        m.addConstr(quicksum(x[i,j,k] for j in range(number_job) ) <= 1)

for i in range(number_machine):
    for k in range(1,UB):
        m.addConstr(quicksum(x[i,j,k] for j in range(number_job)) - quicksum(x[i,j,k-1] for j in range(number_job) ) <= 0)

for t in range(number_job):
    for j in range(number_job):
        if t != j:
            for i in range(number_machine):
                for k in range(1,UB):
                    m.addConstr(C[j]-C[t] + 1000*(2-x[i,j,k]-x[i,t,k-1])>=processing_time[j])

for j in range(number_job):
    for i in range(number_machine):
        m.addConstr(C[j] >= quicksum(processing_time[j]*x[i,j,k] for k in range(UB)))


for j in range(number_job):
    for t in plist[j]:
        m.addConstr(C[j]-C[t] >= quicksum(processing_time[j]*x[i,j,k] for i in range(number_machine) for k in range(UB) ))


for j in range(number_job):
    m.addConstr(C[j] <= Cmax)



m.optimize()
m.write('lnear_model11.lp')


machine_list =[]
for i in range(number_machine):
    machine_list.append([])
for i in range(number_machine):
  for j in range(number_job):
    for k in range(UB):
        if(x[i,j,k].X == 1):
            machine_list[i].append(j)
        
print(machine_list)

for j in range(number_job):
    print(C[j].X)