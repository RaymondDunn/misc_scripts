[metadata, metafields]=wbLoadMetaFile(pwd);
metadata.fileInfo.numZ = metadata.fileInfoOverride.numZ;
metadata.fileInfo.numTInFile = metadata.fileInfoOverride.numT;
save([pwd filesep 'meta.mat'],'-struct','metadata');