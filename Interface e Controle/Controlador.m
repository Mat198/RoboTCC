
% Gma = tf(3.9e4,[1 350 1.5e4]);
Gma = tf(76,[1 29])

% figure(1)
% rlocus(Gma)

Td = 0.02; % 1/45;
K = 18; % 1.26;
Ti = 0.01; %1/(29*16*Td);

% PID = tf([K*Td K K/Ti], [1 0])
% z1 = -4 + 16.7i;
% z2 = conj(z1)
% PID = zpk([z1,z2],0,0.01)
% PID = tf([1 z1+z2 z1*z2], [1 0]
zun = -20
PID = zpk([zun],0,24.6)
figure(2)
rlocus(PID*Gma)

Gmf = feedback(PID*Gma,1)

figure(3)
step(11*Gmf,1.5)