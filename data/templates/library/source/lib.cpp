
#include <iostream>

#include <${proj_name}/${proj_name}-version.h>

#include <${lib_name}/${lib_name}.h>


namespace ${lib_name}
{


void print_version()
{
    std::cout << "Version: " << ${PROJ_NAME}_VERSION << std::endl;
    std::cout << std::endl;
}


} // namespace ${lib_name}
