
# LibRay

LibRay: A portmanteau of Libre and Blu-Ray

LibRay aims to be a Libre (FLOSS) Python application for unencrypting, 
extracting, repackaging, and encrypting PS3 ISOs.

A hackable, crossplatform, alternative to ISOTools and ISO-Rebuilder.



[see also](http://www.psdevwiki.com/ps3/Bluray_disc#Encryption) ([archive.fo](https://archive.fo/hN1E6)) 

[7bit encoded int / RLE / CLP](https://github.com/Microsoft/referencesource/blob/master/mscorlib/system/io/binaryreader.cs#L582-L600)

clp = compressed length prefix


## Todo

- Automatically download .ird file if not given
- Docstrings
- Extract ISO (currently doable with `7z x output.iso`
- Test .irds with version < 9
- Custom command to backup all irds available

## Advanced

Figure out the SCSI commands to get data1, if at all possible.


