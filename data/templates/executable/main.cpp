
#include <iostream>

#include <${proj_name}/${proj_name}-version.h>


int main(int /*argc*/, char* /*argv*/[])
{
    // Print version
    std::cout << "Version: " << ${PROJ_NAME}_VERSION << std::endl;
    std::cout << std::endl;

    // Exit
    return 0;
}
