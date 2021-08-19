# BandagedPaper
Putting bandages on PaperMC since 2021
> A fork of paper which is a fork of spigot which is a fork of craftbukkit which is a minecraft server modification

## Building Paperclip
First, all of the build scripts only work on linux/macOS. If for some reason you still use windows, install WSL or figure it out youself.

Download Papercut from the [Releases Page](https://github.com/c0repwn3r/BandagedPaper/releases), and simply run it in a terminal!
```bash
./papercut
```
Give it several minutes to download BandagedPaper and Paper, and run the patch and compilation scripts. **Make sure you have git installed. Otherwise, this will not work.**
Once the script exits, you will find several JAR files in the directory you have been put in. You can ignore most of them, but `paperclip.jar` is the file you want to upload to your server.

## Contributing
As stated above, all build scripts only work on linux/macOS. This assumes that you have basic knowledge of git and linux-based commands.
#### Building development environment
Clone this repo. Then, run the following command:
```
./bandage applyPatches
```
Wait for it to finish, and your development environment has been built. Make any changes you need in ./work/Paper-Server/.
Contribute to Paper as normal, just do your work in ./work/.

**Note: If you create or edit any patches, make sure to rename them and move them into the /patches/ directory of the BandagedPaper folder, or this will not work.**
Make sure to update the names properly - do not keep the paper number. Look at the current patches in /patches/, figure out what number yours needs to be, and rename it to that.

To submit a pull request, run:
```
./bandage clean
git add .
git commit -a -m "your message"
```
and create a pull request for that commit.
