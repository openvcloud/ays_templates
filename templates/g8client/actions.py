from js9 import j


def input(job):
    args = job.model.args
    if not args.get("account") or not args.get("instance"):
        raise j.exceptions.Input("You need to input account and instance arguments %s" % job.service)
    return args


def processChange(job):
    service = job.service
    args = job.model.args
    category = args.pop('changeCategory')
    if category == 'dataschema':
        for key, value in args.items():
            setattr(service.model.data, key, value)
    service.save()
