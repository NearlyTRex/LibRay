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
A Libre (FLOSS) Python application for unencrypting, extracting, repackaging,
and encrypting PS3 ISOs

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Increase verbosity
  -o OUTPUT, --output OUTPUT
                        Output filename
  -k IRD, --ird IRD     Path to .ird file

required arguments:
  -i ISO, --iso ISO     Path to .iso file
```

You need to use an appropriate blu-ray drive: https://rpcs3.net/quickstart (see "Compatible Blu-ray disc drives section").

On some systems (eg. Linux), you can decrypt directly from the disc.

```
libray -i /dev/sr0 -o ps3_game_decrypted.iso
```

Libray will try to download an IRD decryption file for your iso:

Alternatively, you can first rip the disc to an ISO file and then decrypt from the ISO file:

```
libray -i ps3_game.iso -o ps3_game_decrypted.iso
```

Then, if you want to feed it into RPCS3 just extract the contents of the .ISO:

```
7z x nfs_ps3_decrypted.iso
```

And move the resulting folders into the appropriate folder for RPCS3:

- Linux: /home/username/.config/rpcs3/dev_hdd0/disc/

## License

This project is Free and Open Source Software; FOSS, licensed under the GNU General Public License version 3. GPLv3.

## Error!

Help! I get

> ImportError: No module named Crypto.Cipher

or

> ImportError: cannot import name 'byte_string' from 'Crypto.Util.py3compat' (/usr/lib/python3.7/site-packages/Crypto/Util/py3compat.py)

This is due to multiple similarly named python crypto packages, one way to fix it is:

```
sudo pip uninstall crypto
sudo pip uninstall pycrypto
sudo pip install pycrypto
```

## Development

[see also](http://www.psdevwiki.com/ps3/Bluray_disc#Encryption) ([archive.fo](https://archive.fo/hN1E6))

[7bit encoded int / RLE / CLP](https://github.com/Microsoft/referencesource/blob/master/mscorlib/system/io/binaryreader.cs#L582-L600)

clp = compressed length prefix

## Todo

- Extract ISO (currently doable with `7z x output.iso`
- Repackage (unextract) and reencrypt iso?
- Test .irds with version < 9
- Custom command to backup all irds available
- Unit tests

