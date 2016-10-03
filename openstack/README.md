# SDC OpenStack Usage

## Prerequisites

- [Python2.7](https://www.python.org/downloads/)

**Recommended:**

- virtualenv: `pip install virtualenv`


**Create Python virtualenv (Optional):**

NOTE: Working directory must be the folder where this README is located.

```
virtualenv venv-clients
source venv-clients/bin/activate
```

After the script, virtualenv is activated. To exit virtualenv:

```
deactivate
```

**Install OpenStack Python clients:**

```
pip install -r requirements.txt
```

## Exercises

[commandline tools](commandline)
[heat templates](heat)
[heat & python](python)

## Best Practices

**Commandline Tools:**
Pros:
- Easy to use manually
- Difficulties in keeping and passing states

**Heat:**
Pros:
- High performance and easy usability

Cons:
- Instance update is difficult when using loops. Problems with 90 day machine rotation policy.

Best practice:
- Use heat stacks for networks and python scripts for instance creation and rotation.