# LibRay

LibRay: A portmanteau of Libre and Blu-Ray

LibRay aims to be a Libre (FLOSS) Python application for unencrypting, 
extracting, repackaging, and encrypting PS3 ISOs.

A hackable, crossplatform, alternative to ISOTools and ISO-Rebuilder.

## How to install

1. Clone this repository ```git clone https://notabug.org/necklace/libray```

2. Install dependencies with ```sudo pip install -r requirements.txt```

3. Run ```sudo python setup.py install```

Note: You will need Python 3, so you might want to use `python3` and `pip3`.

`libray` is now installed to your path. In the future I'll add this package to pypi.

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

- Automatically download .ird file if not given
- Docstrings
- Extract ISO (currently doable with `7z x output.iso`
- Test .irds with version < 9
- Custom command to backup all irds available
- pypi

## Advanced

Figure out the SCSI commands to get data1, if at all possible.


