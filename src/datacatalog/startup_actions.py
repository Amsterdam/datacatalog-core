import logging


logger = logging.getLogger(__name__)


async def replace_old_identifiers(app):
    old_identifiers = await app.hooks.get_old_identifiers(app=app)
    count = 0
    changed = 0
    for old_id in old_identifiers:
        count += 1
        new_id = await app.hooks.storage_id()
        result = await app.hooks.set_new_identifier(app=app, old_id=old_id, new_id=new_id)
        if result == 'UPDATE 1':
            changed += 1
    logger.info(f'Set new identifiers for {changed} datasets')
    if changed == count:
        return True
    else:
        return False


async def read_write_all(app):
    dataset_iterator = await app.hooks.storage_all(app=app)
    count = 0
    changed = 0
    logger.info('start rewriting datasets')
    async for docid, etag, doc in dataset_iterator:
        canonical_doc = await app.hooks.mds_canonicalize(app=app, data=doc)
        canonical_doc = await app.hooks.mds_before_storage(app=app, data=canonical_doc, old_data=canonical_doc)
        # Let the metadata plugin grab the full-text search representation
        searchable_text = await app.hooks.mds_full_text_search_representation(
            data=canonical_doc
        )
        count += 1
        result = await app.hooks.storage_update(
            app=app, docid=docid, doc=canonical_doc,
            searchable_text=searchable_text, etags={etag},
            iso_639_1_code="nl")
        if result:
            changed += 1
    logger.info(f'read_write for {changed} datasets')
    if changed == count:
        return True
    else:
        return False


async def read_write_set_status_all(app):
    dataset_iterator = await app.hooks.storage_all(app=app)
    count = 0
    changed = 0
    logger.info('start rewriting datasets')
    async for docid, etag, doc in dataset_iterator:
        canonical_doc = await app.hooks.mds_canonicalize(app=app, data=doc)
        canonical_doc = await app.hooks.mds_before_storage(app=app, data=canonical_doc, old_data=canonical_doc)
        # Let the metadata plugin grab the full-text search representation
        searchable_text = await app.hooks.mds_full_text_search_representation(
            data=canonical_doc
        )
        if 'ams:status' not in canonical_doc:
            canonical_doc['ams:status'] = 'beschikbaar'
        count += 1
        result = await app.hooks.storage_update(
            app=app, docid=docid, doc=canonical_doc,
            searchable_text=searchable_text, etags={etag},
            iso_639_1_code="nl")
        if result:
            changed += 1
    logger.info(f'read_write for {changed} datasets')
    if changed == count:
        return True
    else:
        return False

_startup_actions = [
    ("replace_old_identifiers", replace_old_identifiers),
    ("rw_all_2018_11_22", read_write_set_status_all), # add ams:status to all datasets
]


async def run_startup_actions(app):
    for (name, action) in _startup_actions:
        if not await app.hooks.check_startup_action(app=app, name=name):
            result = await action(app)
            if result:
                await app.hooks.add_startup_action(app=app, name=name)

