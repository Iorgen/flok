# TODO describe all configurations
# TODO create parser with passing all fabrics and creators as arguments
# TODO setup library as a package

# Usage instruction 
Copy config.pt.dist to config/config.py
extract for platform your driver and rename it 
### 

## How to add new parser for resource  
- Create inside collection base and collection or/and detail_page py files 
- Inherit base class from BaseChromeDriverParser
- Inside collection or detail parser create class from base class parser and override 
    _parse_page method using below example 
 
``` python
def _parse_page(self):
    result = {
    }
    """

    :return:
    """
    try:
        try:
            # certain page logic
            pass

        except Exception as E:
            self.LOGGER.warning(f"non exist")
            pass

    except Exception as E:
        raise RetrieveInformationFromPageException()
```  

- Add class with links creation for resource to preparation/links/creators.py with create_links method
- Add link creator to the fabric in page and collection blocks 

