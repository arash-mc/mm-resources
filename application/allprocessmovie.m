path = [pwd '/'];
ff = fopen('list.txt' , 'r');
a = fscanf(ff , '%s');
fclose(ff);
folders = strsplit(a , ',');
folders = sort(folders);
dat = {};
for ss= 1:size(folders , 2)
    folder = folders{ss};
    v = VideoReader([path folder '/' folder '.avi']);
    i = 1;
while v.hasFrame
    img = v.readFrame;
	img = img(130:end , 1500:1503 , 3);
	temp(i) = sum(sum(img>250));  
    i = i+1;
end
 dat{ss} = temp;
 kk = char([]);
 
end 
nn = strsplit(pwd , '/');
save([nn{end} '.mat'])