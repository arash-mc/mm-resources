function allmakemovie2j(folders)
for ss= 1:length(folders)
    
    folder = folders{ss};
     d = dir([folder  '/*.jpg']);
     siz = size(d);
    outVideo = VideoWriter([ folder  '/' folder '.avi']);
    outVideo.FrameRate = 25;
    open(outVideo);
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
   img =  imread([ folder '/' kk(i , :)]);
   writeVideo(outVideo,img);
    end 
    
end
close(outVideo);
 clear kk outVideo
 
end 
save data
 