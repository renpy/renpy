#pragma once

void *load_live2d_object(const char *sofile);
void *load_live2d_function(void *obj, const char *name);
void deallocate_live2d_moc(void *moc);
void deallocate_live2d_model(void *model);
