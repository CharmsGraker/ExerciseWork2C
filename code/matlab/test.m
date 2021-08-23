ts=0:500;
x0=[0.01, 0.99];
[t,x]=ode45('ill',ts,x0);
r=1-x(:,1)-x(:,2);
plot(t,x(:,1),t,x(:,2),ts,r),grid
legend('i(t)','s(t)','r(t)')
