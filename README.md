# LibRay

LibRay: A portmanteau of Libre and Blu-Ray

LibRay aims to be a Libre (FLOSS) Python application for unencrypting,
extracting, repackaging, and encrypting PS3 ISOs.

A hackable, crossplatform, alternative to ISOTools and ISO-Rebuilder.

**Note: this is still a very beta project, report any bug you see!**

## How to install

Note: You will need Python 3, so you might want to use `python3` and `pip3` instead of `python` and `pip` depending on your system.

### From PyPi:

1. `sudo pip install libray`

### Manually:

1. Clone this repository ```git clone https://notabug.org/necklace/libray```

2. Install dependencies with ```sudo pip install -r requirements.txt```

3. Run ```sudo python setup.py install```

### From AUR:

For Arch or Arch-based GNU/Linux distributions there's an option to [install libray from the AUR](https://aur.archlinux.org/packages/libray-git/) (Arch User Repository).

You will need an [AUR helper](https://wiki.archlinux.org/index.php/AUR_helpers) (of which there are many).

Then you will need to run the appropriate install command for that AUR helper using `libray-git` as package name.

This will essentially automatically do the manual method for you.

### Done!

`libray` is now installed to your path.

## How do I use it?

```
usage: libray [-h] -i ISO [-o OUTPUT] [-k IRD] [-d DECRYPTION_KEY] [-v] [-q]

A Libre (FLOSS) Python application for unencrypting, extracting, repackaging,
and encrypting PS3 ISOs

required arguments:
  -i ISO, --iso ISO     Path to .iso file or stream

optional arguments:
  -o OUTPUT, --output OUTPUT
                        Output filename
  -k IRD, --ird IRD     Path to .ird file
  -d DECRYPTION_KEY, --decryption-key DECRYPTION_KEY
                        Manually specify key
  -v, --verbose         Increase verbosity
  -q, --quiet           Quiet mode, only prints on error
```

First off, even before you install libray, you will need a compatible Blu-Ray drive that can read PS3 discs.

There's a compiled list of compatible drives here: [https://rpcs3.net/quickstart](https://rpcs3.net/quickstart) ([archive](https://web.archive.org/web/20190801060739/https://rpcs3.net/quickstart])) (see "Compatible Blu-ray disc drives section").

### 1. Decrypt

On some systems (eg. Linux), you can decrypt directly from the disc.

```
libray -i /dev/sr0 -o ps3_game_decrypted.iso
```

Libray will automatically try to download an IRD decryption file for your iso. If you don't have internet connection, but you do have an .ird file you can specify that:

```
libray -i /dev/sr0 -k game_ird_file.ird -o ps3_game_decrypted.iso
```

Alternatively, you can first rip the disc to an ISO file and then decrypt from the ISO file:

```
libray -i ps3_game.iso -o ps3_game_decrypted.iso
```

If libray is unable to download an .ird for your game, you could manually give it the key, if you have it:

```
libray -i ps3_game.iso -d DECRYPTION_KEY -o ps3_game_decrypted.iso
```

### 2. Extract decrypted ISO

Then, if you want to feed it into RPCS3 just extract the contents of the .ISO:

```
7z x nfs_ps3_decrypted.iso
```

And move the resulting folders into the appropriate folder for RPCS3:

- Linux: /home/username/.config/rpcs3/dev_hdd0/disc/

## License

This project is Free, Libre, and Open Source Software; FLOSS, licensed under the GNU General Public License version 3. GPLv3.

See also COPYING or LICENSE.txt

Copyright © 2018 - 2019 Nichlas Severinsen

## Error!

Help! I get

> ImportError: No module named Crypto.Cipher

or

> ImportError: cannot import name 'byte_string' from 'Crypto.Util.py3compat' (/usr/lib/python3.7/site-packages/Crypto/Util/py3compat.py)

This is due to multiple similarly named python crypto packages, one way to fix it is:

```
sudo pip uninstall crypto
sudo pip uninstall pycrypto
sudo pip install pycryptodome
```

If you get any other errors, or have any other problem with libray, please [create an issue](https://notabug.org/necklace/libray/issues/new)!

## Development

[see also](http://www.psdevwiki.com/ps3/Bluray_disc#Encryption) ([archive.fo](https://archive.fo/hN1E6))

[7bit encoded int / RLE / CLP](https://github.com/microsoft/referencesource/blob/1acafe20a789a55daa17aac6bb47d1b0ec04519f/mscorlib/system/io/binaryreader.cs#L582-L600)

clp = compressed length prefix

## Todo

- Extract ISO (currently doable with `7z x output.iso`)
- Repackage (unextract) and reencrypt iso?
- Test .irds with version < 9
- Custom command to backup all irds available
- Unit tests

