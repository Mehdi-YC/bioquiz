delete from Bioquiz_question;
update sqlite_sequence set seq = 1 where name = 'Bioquiz_question';
insert into bioquiz_question(id ,question ,category ,imagefield ,point,n_answer ,n_image ,Quiz_name ,Id_images ,Correct_answer) values(1 ,"Which kind of microscopy was used to take the following images ?", "microscopy", "mode" ,1,4 ,3 ,"Microscopy" ,"124,134,117", 3);
insert into bioquiz_question(id ,question ,category ,imagefield ,point,n_answer ,n_image ,Quiz_name ,Id_images ,Correct_answer) values(2 ,"Which feature is common between the images ?", "component" ,"component" ,3 ,4 ,2, "Organelles", "12,110", 5);
