#include "pyfreetype.h"
#include <stdio.h>

#undef __FTERRORS_H__
#define FT_ERRORDEF( e, v, s )  { e, s },
#define FT_ERROR_START_LIST
#define FT_ERROR_END_LIST       { 0, 0 }
const struct {
	int          err_code;
	char*  err_msg;
} ft_errors[] = {
#include FT_ERRORS_H
};


char *freetype_error_to_string(int code) {

    int i = 0;

    while (1) {

    	if (ft_errors[i].err_code == code) {
    		return ft_errors[i].err_msg;
    	}

    	if (ft_errors[i].err_msg == NULL) {
    		return "unknown error";
    	}

    	i += 1;
    }
}
