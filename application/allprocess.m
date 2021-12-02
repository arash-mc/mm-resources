path = [pwd '/'];
ff = fopen('list.txt' , 'r');
a = fscanf(ff , '%s');
fclose(ff);
folders = strsplit(a , ',');
for ss= 1:length(folders)
    folder = folders{ss};
     d = dir([path  folder  '/*.bmp']);
     siz = size(d);
     counter = 1;
for i = 1:siz
    if(length(d(i).name) == 11)
    kk(counter , :) = d(i).name;
    end
    counter = counter + 1;
end
kk = sortrows(kk);
siz = size(kk);
temp = zeros(1 , siz(1));
for i = 1:siz(1)
    if strcmp(kk(i , 1), 'm')
   img =  imread([path folder '/' kk(i , :)]);
   temp(i) = sum(sum(img(: , : , 3)));
    end 
    
end
 data{ss} = temp;
 kk = [];
 
end 
save data
 