import os
import shutil
import sys
import glob
import atexit

paperCloned = False
patchesCopied = False
patchesApplied = False
obfedJarGenerated = False
paperclipJarGenerated = False
clean = False
if (os.path.isfile("./bandage.lock")):
    lockfile = open("./bandage.lock", "r")
    lockdata = lockfile.read()
    lockfile.close()
    lda = lockdata.split(";")
    for lock in lda:
        ld = lock.split(",")
        if (ld[0] == "pc"):
            if (ld[1] == "0"):
                paperCloned = False
            else:
                paperCloned = True
        elif (ld[0] == "pcp"):
            if (ld[1] == "0"):
                patchesCopied = False
            else:
                patchesCopied = True
        elif (ld[0] == "pa"):
            if (ld[1] == "0"):
                patchesApplied = False
            else:
                patchesApplied = True
        elif (ld[0] == "ojg"):
            if (ld[1] == "0"):
                obfedJarGenerated = False
            else:
                obfedJarGenerated = True
        elif (ld[0] == "pjg"):
            if (ld[1] == "0"):
                paperclipJarGenerated = False
            else:
                paperclipJarGenerated = True

def getBSLFromBool(data):
    if (data):
        return "1"
    else:
        return "0"

def exit_handler():
    global clean
    if (clean):
        return
    ds = "pc," + getBSLFromBool(paperCloned) + ";pcp," + getBSLFromBool(patchesCopied) + ";pa," + getBSLFromBool(patchesApplied) + ";ojg," + getBSLFromBool(obfedJarGenerated) + ";pjg," + getBSLFromBool(paperclipJarGenerated)
    f = open("./bandage.lock", "w")
    f.write(ds)
    f.close()

atexit.register(exit_handler)

def makePapercut(force):
  with open("papercut", "w") as f:
    f.write("#!/bin/bash\ngit clone https://github.com/c0repwn3r/BandagedPaper\ncd BandagedPaper\n./bandage paperclip")
    os.system("chmod +x papercut")
    print("[Papercut/INFO] Generated papercut file")

def clonePaper(force):
    global paperCloned
    if (paperCloned and not force):
        print("[BPDownloader/FATAL] PaperMC already cloned. If this is incorrect or you want to overwrite the existing Paper build, run again with 'force'")
        sys.exit(-1)
    print("[BPDownloader/INFO] Downloading PaperMC")
    if (os.path.isdir("./work")):
        shutil.rmtree("./work")
    if (os.WEXITSTATUS(os.system("git clone https://github.com/PaperMC/Paper work")) != 0):
        print("[BPDownloader/FATAL] Failed to download PaperMC. See above messages for information.")
        sys.exit(-1)
    else:
        print("[BPDownloader/INFO] PaperMC cloned into ./work")
        paperCloned = True

def copyPatches(force):
    global paperCloned
    global patchesCopied
    if (paperCloned != True):
        clonePaper(force)
    if (patchesCopied and not force):
        print("[BPCPatches/FATAL] Patches already copied. If this is incorrect or you want to overwrite the existing patches, run again with 'force'")
        sys.exit(-1)
    print("[BPCPatches/INFO] Copying patches")
    for filename in os.listdir("./patches"):
        if (filename.endswith(".patch") != True):
            print("[BPCPatches/WARN] File " + filename + " ignored because it is not a patch file")
            continue
        print("[BPCPatches/INFO] Copied patch " + filename)
        shutil.copyfile("./patches/" + filename, "./work/patches/server/" + filename)
    print("[BPCPatches/INFO] Copied patches")
    patchesCopied = True

def applyPatches(force):
    global patchesCopied
    global patchesApplied
    if (patchesCopied != True):
        copyPatches(force)
    if (patchesApplied and not force):
        print("[BPPatcher/FATAL] Patches already applied. If this is incorrect or you want to re-patch, run again with 'force'")
        sys.exit(-1)
    print("[BPPatcher/INFO] Applying patches")
    os.chdir("./work")
    if (os.WEXITSTATUS(os.system("./gradlew applyPatches")) != 0):
        print("[BPPatcher/FATAL] Patching failed. See above messages for information.")
        sys.exit(-1)
    os.chdir("../")
    print("[BPPatcher/INFO] Patches applied successfully")
    patchesApplied = True

def reobfJar(force):
    global patchesApplied
    global obfedJarGenerated
    if (patchesApplied != True):
        applyPatches(force)
    if (obfedJarGenerated and not force):
        print("[BPJarGenerator/FATAL] Obfuscated jar already generated. If this is incorrect or you want to overwrite existing jar, run again with 'force'")
        sys.exit(-1)
    print("[BPJarGenerator/INFO] Reobfuscating jar")
    os.chdir("./work")
    if (os.WEXITSTATUS(os.system("./gradlew reobfJar")) != 0):
        print("[BPJarGenerator/FATAL] Jar generation failed. See above messages for information.")
        sys.exit(-1)
    os.chdir("../")
    for f in glob.glob("./work/Paper-Server/build/libs/*.jar"):
        shutil.copy(f, "./")
    print("[BPJarGenerator/INFO] Generated obfuscated jar successfully.")
    obfedJarGenerated = True

def paperclip(force):
    global obfedJarGenerated
    global paperclipJarGenerated
    if (obfedJarGenerated != True):
        reobfJar(force)
    if (paperclipJarGenerated and not force):
        print("[BPPaperclipGenerator/FATAL] Paperclip jar already generated. If this is incorrect or you want to overwrite existing jar, run again with 'force'")
        sys.exit(-1)
    print("[BPPaperclipGenerator/INFO] Generating paperclip jar")
    os.chdir("./work")
    if (os.WEXITSTATUS(os.system("./gradlew paperclip")) != 0):
        print("[BPPaperclipGenerator/FATAL] Paperclip jar generation failed. See above messages for information.")
        sys.exit(-1)
    os.chdir("../")
    for f in glob.glob("./work/build/libs/*.jar"):
        shutil.copy(f, "./paperclip.jar")
    print("[BPPaperclipGenerator/INFO] Generated paperclip jar successfully.")
    paperclipJarGenerated = True

def clean(force):
    global clean
    for f in glob.glob("./*.jar"):
        os.remove(f)
    shutil.rmtree("./work")
    os.remove("bandage.lock")
    clean = True
    sys.exit(0)

def makeGitCommit(force):
  print("[BandagedGit] Removing files to regenerate them.")
  clean()
  os.system("rm -rf bandage papercut")
  print("[BandagedGit] Regenerating bandage")
  with open("bandage", "w") as f:
    f.write("#!/bin/bash\npython bandage.py \"$@\"")
  os.system("chmod +x bandage")
  print("[BandagedGit] Regenerating papercut")
  makePapercut(False)
  print("[BandagedGit] Building")
  paperclip()

if (len(sys.argv) == 1):
    print("Usage: ./bandage <clonePaper|copyPatches|applyPatches|reobfJar|paperclip> [force]")
    print("Avaliable tasks:")
    print("clonePaper - Clones paper from upstream repository.")
    print("copyPatches - Copies BandagedPaper patches into PaperMC patch scripts.")
    print("applyPatches - Apply patches.")
    print("reobfJar - Generate real jars and place them in root directory.")
    print("paperclip - Generate paperclip jars.")
    print("clean - Delete all output files.")
    print("papercut - Generate papercut")
    print("git - Generate Git PR commit")
    print("-----")
    print("Add 'force' to the end of a command to force it to run even if files already exist.")
    sys.exit(0)
if (len(sys.argv) > 3):
    print("Usage: ./bandage <clonePaper|copyPatches|applyPatches|reobfJar|paperclip> [force]")
    print("Avaliable tasks:")
    print("clonePaper - Clones paper from upstream repository.")
    print("copyPatches - Copies BandagedPaper patches into PaperMC patch scripts.")
    print("applyPatches - Apply patches.")
    print("reobfJar - Generate real jars and place them in root directory.")
    print("paperclip - Generate paperclip jars.")
    print("clean - Delete all output files.")
    print("papercut - Generate papercut")
    print("git - Generate Git PR commit")
    print("-----")
    print("Add 'force' to the end of a command to force it to run even if files already exist.")
    sys.exit(0)

commands = {
        "clonePaper": clonePaper,
        "copyPatches": copyPatches,
        "applyPatches": applyPatches,
        "reobfJar": reobfJar,
        "paperclip": paperclip,
        "clean": clean,
        "papercut": makePapercut,
        "git": makeGitCommit
    }

if (sys.argv[1] not in commands):
    print("Unknown command '" + sys.argv[1] + "'.")
    print("Usage: ./bandage <clonePaper|copyPatches|applyPatches|reobfJar|paperclip> [force]")
    print("Avaliable tasks:")
    print("clonePaper - Clones paper from upstream repository.")
    print("copyPatches - Copies BandagedPaper patches into PaperMC patch scripts.")
    print("applyPatches - Apply patches.")
    print("reobfJar - Generate real jars and place them in root directory.")
    print("paperclip - Generate paperclip jars.")
    print("clean - Delete all output files.")
    print("papercut - Generate papercut")
    print("git - Generate Git PR commit")
    print("-----")
    print("Add 'force' to the end of a command to force it to run even if files already exist.")
    sys.exit(0)
else:
    if (len(sys.argv) == 3 and sys.argv[2] == "force"):
        commands[sys.argv[1]](True)
    else:
        commands[sys.argv[1]](False)
