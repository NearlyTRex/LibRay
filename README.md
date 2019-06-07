# LibRay

LibRay: A portmanteau of Libre and Blu-Ray

LibRay aims to be a Libre (FLOSS) Python application for unencrypting, 
extracting, repackaging, and encrypting PS3 ISOs.

A hackable, crossplatform, alternative to ISOTools and ISO-Rebuilder.

**Note: this is still a very beta project, report any bug you see!**

## How to install

1. Clone this repository ```git clone https://notabug.org/necklace/libray```

2. Install dependencies with ```sudo pip install -r requirements.txt```

3. Run ```sudo python setup.py install```

Note: You will need Python 3, so you might want to use `python3` and `pip3`.

`libray` is now installed to your path. In the future I'll add this package to pypi.

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

Rip a PS3 to .ISO with an appropriate blu-ray drive: https://rpcs3.net/quickstart (see "Compatible Blu-ray disc drives section"). 
Then just feed the .ISO to libray which will try to download an IRD decryption file for your iso. 

Example:

```
libray -i ps3_game.iso -o ps3_game_decrypted.iso
```

Then, if you want to feed it into RPCS3 just extract the contents of the .ISO:

```
7z x nfs_ps3_decrypted.iso
```

And move the resulting folders into the appropriate folder for RPCS3.

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

- Docstrings
- Extract ISO (currently doable with `7z x output.iso`
- Repackage (unextract) and reencrypt iso?
- Test .irds with version < 9
- Custom command to backup all irds available
- pypi
