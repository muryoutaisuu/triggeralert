# triggeralert

Splunk App for manually triggering a Splunk Alert.

_Hint: This script just prematurely triggers an alert. The alert condition has to match for an actual event to take place! Beware that throttling will be complied with!_

## Use Cases

* testing alerts
* prematurely triggering reports
* trigger a missed alert

## Usage

**Parameter**|**Description**|**Default**|**Example**
:-----|:-----|:-----|:-----
`app="<appname>"`|app name in which the alert is located|app in which the command is used|`triggeralert name="myAlert" app="myApp"`
`esc`|`$` characters will be translated into blanks. Used for searches with blankspaces in their names|unset|`triggeralert name="my$Alert" app="my$App" esc`
`name="<alertname>"`|alert name that should be triggered|unset|`triggeralert name="myAlert"`

No output will be shown on successfull run.

## Examples

name of testalert shall be `myTestAlert` located in app `myApp`:

```bash
| triggeralert name="myTestAlert" app="myApp"
```
