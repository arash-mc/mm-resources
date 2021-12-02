path = [pwd '/'];
ff = fopen('list.txt' , 'r');
a = fscanf(ff , '%s');
fclose(ff);
folders = strsplit(a , ',');
folders = sort(folders);
dat = {};
for ss= 1:size(folders , 2)
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
		img = img(130:end , 1250:1260 , 3);
		temp(i) = sum(sum(img));
    end 
    
end
 dat{ss} = temp;
 kk = char([]);
 
end 
nn = strsplit(pwd , '/');
save(nn{end});
 